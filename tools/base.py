from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, List
from langchain.tools import BaseTool as LangChainBaseTool

class BaseTool(ABC):
    """Base class for all tools in the system."""
    
    name: str
    description: str
    
    @abstractmethod
    def _run(self, *args: Any, **kwargs: Any) -> Any:
        """Implementation of the tool functionality."""
        pass
    
    def to_langchain_tool(self) -> LangChainBaseTool:
        """Convert to a LangChain tool format."""
        from langchain.tools import Tool
        
        # Create a proper Tool instance rather than using the decorator
        # This provides better type safety and control
        tool = Tool(
            name=self.name,
            description=self.description,
            func=lambda input_str, **kwargs: self._run(input_str, **kwargs)
        )
        
        return tool