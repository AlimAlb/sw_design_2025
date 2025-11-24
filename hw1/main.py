from ui import UI, FirstOption, AnimalsOptions, InventoryOptions
from animal_classes import Monkey, Wolf, Tiger, Rabbit
from interfaces import IAlive, IInventory
from inventory_classes import Table, Computer
from vet_clinic import Vetclinic
from zoo import Zoo
from di_container import di_container
import random as rnd
from typing import cast, Tuple

def main() -> None:
    di = di_container()
    scoped = [Monkey, Wolf, Tiger, Rabbit]
    singletones = [Table, Computer, Vetclinic, Zoo, UI]

    for tp in scoped:
        di.register(tp, singleton=False)
    for tp in singletones:
        di.register(tp, singleton=True)
    
    zoo = cast(Zoo, di.resolve(Zoo))
    zoo.load_state()
    vet_clinic = di.resolve(Vetclinic, func = lambda x: rnd.random() > .5)
    ui = UI()
    on_start = True
    while True:
        if on_start:
            ui.start()
            on_start = False
        main_option = ui.main_menu()

        if main_option == FirstOption.ANIMALS:
            animal_option = ui.animals_menu()
            if animal_option == AnimalsOptions.ADD:
                obj = cast(Tuple[bool, IAlive], ui.add_animal(di))
                if obj[0]:
                    animal = cast(IAlive, obj[1])
                    zoo.add_animal(animal)
                
            elif animal_option == AnimalsOptions.SHOW_ALL:
                ui.show_zoo(zoo)
            elif animal_option == AnimalsOptions.SHOW_CONTACT:
                ui.show_contact(zoo)
            elif animal_option == AnimalsOptions.SHOW_FOOD:
                ui.show_food(zoo)

        elif main_option == FirstOption.INVENTORY:
            inv_option = ui.inventory_menu()
            if inv_option == InventoryOptions.ADD:
                obj = ui.add_inventory(di)
                zoo.add_inventory(cast(IInventory, obj))
            elif inv_option == InventoryOptions.SHOW_ALL:
                ui.show_inventory(zoo)

        elif main_option == FirstOption.EXIT:
            zoo.save_state()
            break



main()