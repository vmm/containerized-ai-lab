from typing import Any
import re
from .base import BaseTool

class CalculatorTool(BaseTool):
    """A tool for performing basic calculations."""
    
    name = "calculator"
    description = "Useful for performing arithmetic calculations. Input should be a mathematical expression like '1 + 2' or '3 * 4'."
    
    def _run(self, expression: str, **kwargs: Any) -> str:
        """Evaluate a mathematical expression."""
        try:
            # Clean up the expression by removing equals signs and other non-math characters
            clean_expr = expression.strip()
            
            # Remove trailing equals sign if present
            if clean_expr.endswith('='):
                clean_expr = clean_expr[:-1].strip()
            
            # Only allow valid math expressions with basic operators and numbers
            if not re.match(r'^[\d\s\+\-\*\/\(\)\.\%\*\*]+$', clean_expr):
                return f"Invalid expression. Please provide a simple math expression using +, -, *, /, (, ), or **."
            
            # Using eval is generally not recommended in production
            # In a real implementation, consider a safer alternative like the `ast.literal_eval` 
            # or a dedicated math expression parser
            result = eval(clean_expr)
            return str(result)
        except Exception as e:
            return f"Error calculating result: {str(e)}"