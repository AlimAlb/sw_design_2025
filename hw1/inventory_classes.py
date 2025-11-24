from interfaces import IInventory
from uuid import uuid4

class Thing(IInventory):
    def __init__(self, number: int):
        if number >= 0:
            self._number = number
        else:
            raise ValueError(f"Number should be non-negative, not {number}")
        
        self._id = uuid4()

    
    @property
    def number(self) -> int:
        return self._number
    
    def add(self, number: int) -> None:
        self._number += number

    def __str__(self) -> str:
        return f"type: {type(self).__name__} \t id (first digits): {str(self._id)[:8]} \t number: {self._number}"

class Table(Thing):
    pass

class Computer(Thing):
    pass