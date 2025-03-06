from typing import Any
from .base import BaseTool

class WebSearchTool(BaseTool):
    """A tool for performing web searches."""
    
    name = "web_search"
    description = "Useful for searching the web for information. Input should be a search query."
    
    # Mock search database for demonstration purposes
    MOCK_DB = {
        "weather": "The current weather is sunny with a high of 75°F.",
        "news": "Latest headlines: Tech stocks rise, new climate policy announced, sports team wins championship.",
        "recipe": "Popular recipes: pasta carbonara, chicken curry, chocolate cake.",
        "math": "Math concepts: algebra, calculus, statistics, geometry.",
        "computer": "Computer science topics: programming, algorithms, data structures, artificial intelligence.",
        "ai": "AI development is advancing rapidly with new models being released regularly.",
        "docker": "Docker is a platform for developing, shipping, and running applications in containers.",
        "python": "Python is a popular programming language known for its readability and versatility. It's widely used for web development, data science, machine learning, and automation. Python has a simple syntax that makes it easy to learn, and it has a large ecosystem of libraries and frameworks.",
        "movies": "Recent popular movies include action, drama, and comedy genres.",
        "books": "Bestselling books span fiction, non-fiction, self-help, and fantasy categories.",
        "programming": "Programming is the process of creating software using programming languages. Popular languages include Python, JavaScript, Java, C++, and many others.",
        "data science": "Data science combines statistics, programming, and domain knowledge to extract insights from data. It often uses Python and R languages.",
        "web development": "Web development involves creating websites and web applications. It typically uses HTML, CSS, JavaScript, and various frameworks and libraries.",
        "artificial intelligence": "Artificial intelligence involves creating systems that can perform tasks that typically require human intelligence. This includes machine learning, natural language processing, and computer vision.",
        "machine learning": "Machine learning is a subset of AI that involves training systems to learn from data and make predictions or decisions without being explicitly programmed.",
        "containerization": "Containerization is a technology for packaging and running applications and their dependencies in isolated environments called containers.",
    }
    
    def _run(self, query: str, **kwargs: Any) -> str:
        """
        Simulates a web search using a mock database.
        
        In a real implementation, you would integrate with a search API like:
        - Bing Search API
        - Google Custom Search API
        - DuckDuckGo API
        """
        query = query.lower().strip()
        
        # Check for basic math queries (redirect to calculator)
        if any(op in query for op in ['+', '-', '*', '/', 'calculate', 'computation']):
            return "This seems like a math question. Please use the calculator tool instead."
        
        # Try to match the query with our mock database
        results = []
        for key, value in self.MOCK_DB.items():
            if key in query:
                results.append(f"Result for '{key}': {value}")
        
        # If we have specific results, return them
        if results:
            return "\n\n".join(results)
        
        # Generic response for other queries
        return f"Simulated search results for: {query}\n\n" + \
               "1. The information you're looking for could be found on various websites.\n" + \
               "2. Several articles discuss this topic with different perspectives.\n" + \
               "3. There are forums and communities where people share information about this."