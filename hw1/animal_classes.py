from interfaces import IAlive
from uuid import uuid4

class Animal(IAlive):
    def __init__(self, food: int, is_healthy: bool):
        if  food >= 0: 
            self._food = food
        else:
            raise ValueError('food should be non negative')
        self._is_healthy = is_healthy
        self._id = uuid4()
    
    @property
    def food(self) -> int:
        return self._food
    
    def __str__(self) -> str:
        return f"type: {type(self).__name__} \t id (first digits): {str(self._id)[:8]} \t food: {self._food} \t healthy:{'yes' if self._is_healthy else 'no'}"
    
    

class Herbo(Animal):
    def __init__(self, food: int, is_healthy: bool, wellness: int):
        super().__init__(food, is_healthy)
        if  0<= wellness <= 10:
            self._wellness = wellness
    
    @property
    def wellness(self) -> int:
        return self._wellness

    def __str__(self) -> str:
        return super().__str__() + f" \t welness: {self._wellness}"
    


class Predator(Animal):
    def __init__(self, food: int, is_healthy: bool):
        super().__init__(food, is_healthy)

# Those classes doesnt have any additional logic so we just inherit them from base classes 
class Monkey(Herbo):
    pass

class Rabbit(Herbo):
    pass

class Tiger(Predator):
    pass

class Wolf(Predator):
    pass

    

    
