from typing import Protocol

class Animal(Protocol):
    def eat(self) -> None:
        ...


class Bird:
    def eat(self) -> None:
        print('smth')

