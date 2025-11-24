import sys
import time
import itertools
from typing import Union, Tuple, cast
import os
from enum import Enum
from zoo import Zoo
from animal_classes import *
from inventory_classes import *
from vet_clinic import Vetclinic
import logging
from di_container import di_container

class FirstOption(Enum):
    ANIMALS = 1
    INVENTORY = 2
    EXIT = 3

class AnimalsOptions(Enum):
    ADD = 1
    SHOW_ALL = 2
    SHOW_CONTACT = 3
    SHOW_FOOD = 4

class InventoryOptions(Enum):
    ADD = 1
    SHOW_ALL = 2


class UI:
    animal_types = [Monkey, Wolf, Rabbit, Tiger]
    inv_types = [Computer, Table]
    def __init__(self):
        self.__logger = self.__set_logger()

    def main_menu(self) -> FirstOption:
        self.clear()
        print("Choose an option:")
        print("1. Animals")
        print("2. Items")
        print("3. Exit")
        s = input('(Input a number) >> ')
        option = 0
        while True:
            try:
                option = int(s)
                if option in [1,2,3]:
                    break
            except:
                self.__logger.error('Casting error')
                print('Should be a number 1-2')
            print('Should be a number 1-2')
            self.__logger.error('Wrong number')
            s = input('(Input a number) >> ')
        
        return FirstOption(option)
        
            
    def animals_menu(self) -> AnimalsOptions:
        self.clear()
        print('Choose an option:')
        print('1. Add an animal')
        print('2. Show all animals')
        print('3. Show animals for contact zoo')
        print('4. Show needed amout of food')
        s = input('(Input a number) >> ')
        option = 0
        while True:
            try:
                option = int(s)
                if option in AnimalsOptions._value2member_map_:
                    break
            except:
                self.__logger.error('Casting error')
                print('Should be a number 1-4')
            
            print('Should be a number 1-4')
            self.__logger.error('Wrong number')
            s = input('(Input a number) >> ')
        return AnimalsOptions(option)

    def inventory_menu(self) -> InventoryOptions:
        self.clear()
        print('Choose an option:')
        print('1. Add an item')
        print('2. Show all items')
        s = input('(Input a number) >> ')
        option = 0
        while True:
            try:
                option = int(s)
                if option in AnimalsOptions._value2member_map_:
                    break
            except:
                self.__logger.error('Casting error')
                print('Should be a number 1-2')
            
            print('Should be a number 1-2')
            self.__logger.error('Wrong number')
            s = input('(Input a number) >> ')
        return InventoryOptions(option)

    def show_zoo(self, zoo: Zoo) -> None:
        self.clear()
        items = zoo.list_all_animals()
        print('List of all animals:')
        for item in items:
            print(item)
        input('Press Enter to leave...')
        self.__logger.info('listed all animals')

    def show_inventory(self, zoo: Zoo) -> None:
        self.clear()
        items = zoo.list_all_inventory()
        print('List of all inventory:')
        for item in items:
            print(item)
        input('Press Enter to leave...')
        self.__logger.info('listed all inventory')

    def show_contact(self, zoo: Zoo) -> None:
        self.clear()
        items = zoo.are_in_good_mood()
        print("List of all animals for contact zoo:")
        for item in items:
            print(item)
        input('Press Enter to leave...')
        self.__logger.info('listed all contact animals')

    
    def show_food(self, zoo: Zoo) -> None:
        self.clear()
        print("Amount of food needed (kg):")
        print(zoo.food())
        self.__logger.info('showed total food')
        input('Press Enter to leave...')
    
    def add_animal(self, di: di_container) -> Union[Tuple[bool, IAlive], IInventory, Zoo, Vetclinic]:
        self.clear()
        print('Input animal info separated by commma:')
        print(f'Type: {[t.__name__ for t in self.animal_types]}')
        print(f'Food: positive integer')
        print(f'Welness (only for Herbos): non-negative integer 0-10')
        chunks = input('>> ').split(',')
        obj = None
        while True:
            try:
                if len(chunks) >= 4:
                    raise ValueError('Too much arguments')
                tp = [cls for cls in self.animal_types if cls.__name__ == chunks[0]][0]
                if tp is None:
                    raise ValueError('wrong type of animal')
                food = int(chunks[1])
                if food <= 0:
                    raise ValueError('Food should be positive integer')
            
                if issubclass(tp, Herbo):
                    wellness = int(chunks[2])
                    if not(0<= wellness <= 10):
                        raise ValueError('Wellnes should be integer 1-10')
                    obj = di.resolve(tp, food = food, is_healthy = True, wellness = wellness)
                    self.__logger.info("Herbo created")
                else:
                    if len(chunks) >= 3:
                        raise ValueError('Wrong amout of arguments for Predator')
                    else:
                        obj = di.resolve(tp, food = food, is_healthy = True)
                        self.__logger.info("Predator created")

                break
            
            except Exception as e:
                  self.__logger.error(f'error at adding animal: {e}')
                  print('Wrong input, try again')
            
            chunks = input('>> ').split(', ')
        
        if cast(Tuple[bool, IAlive],obj)[0]:
            print('Ветклиника провела исследование и животное принято')
        else:
            print('Ветклиника провела исследование и животное не принято')
        input('Press Enter to leave...')
        return obj
    
    def add_inventory(self, di: di_container) -> Union[Tuple[bool, IAlive], IInventory, Zoo, Vetclinic]:
        self.clear()
        print('Input inventory info separated by commma:')
        print(f'Type: {[t.__name__ for t in self.inv_types]}')
        print(f'Number: positive integer')
        chunks = input('>> ').split(',')
        obj = None
        while True:
            try:
                if len(chunks) >= 3:
                    raise ValueError('Too much arguments')
                tp = [cls for cls in self.inv_types if cls.__name__ == chunks[0]][0]
                if tp is None:
                    raise ValueError('wrong type of inventory')
                number = int(chunks[1])
                if number <= 0:
                    raise ValueError('Number should be positive integer')
                obj = di.resolve(tp, number=number)
                self.__logger.info(f'inventory created')
                break
            except Exception as e:
                  self.__logger.error(f'error at adding inventory: {e}')
                  print('Wrong input, try again')
            chunks = input('>> ').split(', ')
        return obj
        

    def start(self) -> None:

        spinner = itertools.cycle("⠋⠙⠹⠸⠼⠴⠦⠧⠇⠏")
        try:
            # short spinner "loading"
            for _ in range(30):
                sys.stdout.write("\rЗагрузка " + next(spinner))
                sys.stdout.flush()
                time.sleep(0.07)

            # launching progress bar
            bar_len = 30
            sys.stdout.write("\rЗапуск: [" + " " * bar_len + "]")
            sys.stdout.flush()
            sys.stdout.write("\rЗапуск: [")
            for i in range(bar_len):
                sys.stdout.write("█")
                sys.stdout.flush()
                time.sleep(0.04)
            sys.stdout.write("] Готово\n")
            sys.stdout.flush()
            time.sleep(0.25)
        except KeyboardInterrupt:
            # graceful exit if interrupted
            sys.stdout.write("\n")
            sys.stdout.flush()
            return

    def clear(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        print()

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


