import os
import sys
import unittest

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from animal_classes import Monkey, Tiger


class AnimalTests(unittest.TestCase):
    def test_monkey_food_and_wellness(self):
        monkey = Monkey(food=3, is_healthy=True, wellness=7)
        self.assertEqual(monkey.food, 3)
        self.assertIn("Monkey", str(monkey))
        self.assertIn("welness", str(monkey))

    def test_predator_rejects_negative_food(self):
        with self.assertRaises(ValueError):
            Tiger(food=-1, is_healthy=True)


if __name__ == "__main__":
    unittest.main()
