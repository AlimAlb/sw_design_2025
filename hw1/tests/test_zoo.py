import os
import sys
import tempfile
import unittest

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from animal_classes import Monkey, Tiger
from inventory_classes import Table
from zoo import Zoo


class ZooTests(unittest.TestCase):
    def test_add_animals_inventory_and_food(self):
        zoo = Zoo()
        monkey = Monkey(food=2, is_healthy=True, wellness=8)
        tiger = Tiger(food=5, is_healthy=True)
        table = Table(number=1)

        zoo.add_animal(monkey)
        zoo.add_animal(tiger)
        zoo.add_inventory(table)
        zoo.add_inventory(table)

        animals = zoo.list_all_animals()
        inventory = zoo.list_all_inventory()

        self.assertEqual(zoo.food(), 7)
        self.assertEqual(len(animals), 2)
        self.assertIsNot(animals[0], monkey)
        self.assertEqual(len(inventory), 1)  # duplicate prevented
        self.assertIsNot(inventory[0], table)

    def test_are_in_good_mood_filters_wellness(self):
        zoo = Zoo()
        ok_monkey = Monkey(food=1, is_healthy=True, wellness=6)
        sad_monkey = Monkey(food=1, is_healthy=True, wellness=3)
        zoo.add_animal(ok_monkey)
        zoo.add_animal(sad_monkey)

        good = zoo.are_in_good_mood()
        self.assertEqual(len(good), 1)
        self.assertIsNot(good[0], ok_monkey)

    def test_save_and_load_state_in_temp_dir(self):
        original_cwd = os.getcwd()
        try:
            with tempfile.TemporaryDirectory() as tmp:
                os.chdir(tmp)
                os.makedirs("data", exist_ok=True)

                zoo = Zoo()
                zoo.add_animal(Monkey(food=2, is_healthy=True, wellness=5))
                zoo.add_inventory(Table(number=2))
                zoo.save_state()

                restored = Zoo()
                restored.load_state()

                self.assertEqual(len(restored.list_all_animals()), 1)
                self.assertEqual(len(restored.list_all_inventory()), 1)
        finally:
            os.chdir(original_cwd)


if __name__ == "__main__":
    unittest.main()
