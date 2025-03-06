import os
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import uvicorn
import httpx
from typing import List, Dict, Any

from langchain.agents import AgentExecutor, create_react_agent
from langchain.agents.format_scratchpad import format_to_openai_function_messages
from langchain.agents.output_parsers import OpenAIFunctionsAgentOutputParser, ReActSingleInputOutputParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder, PromptTemplate
from langchain_core.messages import AIMessage, HumanMessage
from langchain_ollama import OllamaLLM
from langchain_core.tools import BaseTool as LangChainBaseTool

# Initialize FastAPI
app = FastAPI(title="Containerized AI Lab")

# Mount static files
app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

# Get environment variables
OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://localhost:11434")
MODEL_NAME = os.getenv("MODEL_NAME", "llama2")
FALLBACK_MODEL = os.getenv("FALLBACK_MODEL", "phi")  # Smaller model as fallback

# Get tools
def get_tools():
    from tools import WebSearchTool, CalculatorTool
    
    # Initialize tools
    web_search = WebSearchTool()
    calculator = CalculatorTool()
    
    # Convert to LangChain format
    return [
        web_search.to_langchain_tool(),
        calculator.to_langchain_tool()
    ]

# Setup LLM and Agent
def create_agent():
    try:
        # Try to load the primary model
        llm = OllamaLLM(
            base_url=OLLAMA_HOST,
            model=MODEL_NAME,
            temperature=0.7,
        )
    except Exception as e:
        print(f"Error loading primary model {MODEL_NAME}: {str(e)}")
        print(f"Falling back to smaller model: {FALLBACK_MODEL}")
        # Fall back to a smaller model
        llm = OllamaLLM(
            base_url=OLLAMA_HOST,
            model=FALLBACK_MODEL,
            temperature=0.7,
        )
    
    tools = get_tools()
    
    # Create a ReAct style prompt which works better with Ollama models
    template = """Answer the following questions as best you can. You have access to the following tools:

{tools}

Use the following format EXACTLY:

Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of [{tool_names}]
Action Input: the exact input to the action with no parentheses, quotes or extra characters
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer (IMPORTANT: once you have enough information, you MUST proceed to the final answer)
Final Answer: the final answer to the original input question

IMPORTANT: You have a maximum of 5 tool uses. You must provide a Final Answer after gathering sufficient information, even if it's not complete.

Here are two examples:

Example 1:
Question: What's 2 + 2?
Thought: I need to calculate this simple math problem.
Action: calculator
Action Input: 2 + 2
Observation: 4
Thought: I now know the final answer.
Final Answer: The answer to 2 + 2 is 4.

Example 2:
Question: What do you know about Python?
Thought: I should search for information about Python.
Action: web_search
Action Input: python
Observation: Python is a popular programming language known for its readability and versatility.
Thought: I now know the final answer.
Final Answer: Python is a popular programming language that is known for being readable and versatile.

Begin!

Question: {input}
{agent_scratchpad}"""

    prompt = PromptTemplate.from_template(template)
    
    # Create the ReAct agent
    agent = create_react_agent(llm, tools, prompt)
    
    return AgentExecutor(
        agent=agent,
        tools=tools,
        verbose=True,
        handle_parsing_errors=True,
        max_iterations=5,  # Limit the number of tool uses
        early_stopping_method="force",  # Force stop after max_iterations
        return_intermediate_steps=True  # Return the reasoning steps
    )

# Create the agent
agent = create_agent()

# API routes
@app.get("/")
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/chat")
async def chat(request: Request):
    data = await request.json()
    user_input = data.get("input", "")
    
    try:
        # Run the agent with just the input
        response = agent.invoke({
            "input": user_input
        })
        
        # Get the output and intermediate steps
        output = response["output"]
        steps = response.get("intermediate_steps", [])
        
        # Format steps for debugging (only in console)
        if steps:
            print("\nAGENT REASONING STEPS:")
            for i, (action, observation) in enumerate(steps):
                print(f"Step {i+1}:")
                print(f"  Action: {action.tool} - {action.tool_input}")
                print(f"  Observation: {observation}")
        
        # Check if we hit the iteration limit without a proper response
        if output == "Agent stopped due to iteration limit or time limit.":
            # Generate a response based on the collected observations
            observations = []
            for _, observation in steps:
                if observation and isinstance(observation, str):
                    observations.append(observation)
            
            if observations:
                # Join unique observations to create a comprehensive answer
                unique_observations = list(set(observations))
                summary = " ".join(unique_observations)
                final_answer = f"Based on my research: {summary}"
            else:
                final_answer = "I apologize, but I wasn't able to find a complete answer to your question."
            
            # Return the synthesized answer
            return JSONResponse(content={"response": final_answer})
        
        # Return the original output if we didn't hit the limit
        return JSONResponse(content={"response": output})
    except Exception as e:
        print(f"Error in chat: {str(e)}")
        return JSONResponse(
            content={"response": f"I'm sorry, I encountered an error processing your request. Please try asking in a different way."},
            status_code=500
        )

@app.get("/models")
async def list_models():
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(f"{OLLAMA_HOST}/api/tags")
            return response.json()
        except Exception as e:
            return {"error": str(e)}

# Run the server
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)