from typing import Protocol


class IAlive(Protocol):
    @property
    def food(self) -> int:
        ...


class IInventory(Protocol):
    @property
    def number(self) -> int:
        ...