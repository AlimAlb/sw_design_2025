from typing import Callable
from animal_classes import *
from interfaces import IAlive


class Vetclinic:
    def __init__(self, func: Callable[[IAlive], bool]):
        self.func = func
    

    def inspect(self, obj) -> bool:
        return self.func(obj)

