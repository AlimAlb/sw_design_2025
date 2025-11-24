from typing import Dict, Union, cast, Tuple
from interfaces import IInventory, IAlive
from inventory_classes import Thing
from vet_clinic import Vetclinic
from zoo import Zoo
from enum import Enum

class Lifetime(Enum):
    SINGLETON = 0
    SCOPED = 1

#TODO: di_container should check if singleton items are created and if so - add number of newly created items to already existing ones
class di_container:
    def __init__(self):
        self.__specification: Dict[type, Lifetime] = {}
        self.__singletons: Dict[type, Union[Tuple[bool, IAlive], IInventory, Thing,  Zoo, Vetclinic]] = {}

    def register(self, cls: type, singleton: bool = False) -> None:
        self.__specification[cls] =  Lifetime.SINGLETON if  singleton else Lifetime.SCOPED

    def resolve(self, cls, **kwargs) -> Union[Tuple[bool, IAlive], IInventory, Zoo, Vetclinic]:
        if self.__specification[cls] is Lifetime.SINGLETON:
            if cls not in self.__singletons:
                self.__singletons[cls] = cls(**kwargs)
            elif issubclass(cls, Thing):
                cast(Thing, self.__singletons[cls]).add(kwargs['number'])
            return self.__singletons[cls]
        elif self.__specification[cls] is Lifetime.SCOPED:
            obj = cls(**kwargs)
            if cast(Vetclinic, self.__singletons[Vetclinic]).inspect(obj):
                return (True, obj)
            else:
                return (False, obj)
        else:
            raise ValueError(f'This type is not registered in {self.__specification}')