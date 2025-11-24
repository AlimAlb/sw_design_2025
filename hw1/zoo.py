from copy import copy
from typing import Union, List
import logging 
from interfaces import IAlive, IInventory
from animal_classes import Herbo
import pickle

class Zoo:
    def __init__(self):
        self.__animals = []
        self.__inventory = []
        self.__logger = self.__set_logger()


    def __set_logger(self) -> logging.Logger:
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.INFO)
        file_handler = logging.FileHandler('app.log')
        file_handler.setLevel(logging.INFO)
        
        formatter = logging.Formatter(
           "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )

        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
        return logger

    
    def add_animal(self, obj: IAlive) -> None:
        self.__animals.append(obj)
    
    def add_inventory(self, obj: IInventory) -> None:
        if obj not in self.__inventory:
            self.__inventory.append(obj)
    
    def food(self) -> int:
        food = 0
        for animal in self.__animals:
            food += animal.food
        return food

    def are_in_good_mood(self) -> List[IAlive]:
        good_moods = []
        for animal in self.__animals:
            if issubclass(type(animal), Herbo):
                if animal.wellness >= 5:
                    good_moods.append(copy(animal))
        return good_moods

    def list_all_animals(self) -> List[IAlive]:
        animals = []
        for animal in self.__animals:
            animals.append(copy(animal))
        return animals
    
    def list_all_inventory(self) -> List[IInventory]:
        inv = []
        for item in self.__inventory:
            inv.append(copy(item))
        return inv
    
    
    
    def save_state(self):
        self.__logger.info('starting saving state')
        try:
            with open('data/animals.plk', 'wb') as file:
                pickle.dump(self.__animals, file)
                self.__logger.info("State of animals saved")
        except Exception as e:
            self.__logger.error(f"Smth went wrong with animals: {e}")
        try:
            with open('data/inventory.plk', 'wb') as file:
                pickle.dump(self.__inventory, file)
                self.__logger.info("State of inventory saved")
        except Exception as e:
            self.__logger.error(f"Smth went wrong with inventory: {e}")
        self.__logger.info('state of the zoo saved')

    def load_state(self):
        self.__logger.info('starting loading state')
        try:
            with open('data/animals.plk', 'rb') as file:
                self.__animals = pickle.load(file)
                self.__logger.info("State of animals loaded")
        except Exception as e:
            self.__logger.error(f"Smth went wrong with animals: {e}")
        try:
            with open('data/inventory.plk', 'rb') as file:
                self.__inventory = pickle.load(file)
                self.__logger.info("State of inventory loaded")
        except Exception as e:
            self.__logger.error(f"Smth went wrong with inventory: {e}")
        self.__logger.info('state of the zoo loaded')