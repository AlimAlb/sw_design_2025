"""Base command interface."""
from abc import ABC, abstractmethod
from typing import Any



class Command(ABC):
    """Abstract command interface."""
    
    @abstractmethod
    def execute(self) -> Any:
        """Execute the command."""
        pass



