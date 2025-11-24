import os
import sys
import unittest

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from inventory_classes import Table, Thing


class InventoryTests(unittest.TestCase):
    def test_table_number_and_add(self):
        table = Table(number=2)
        self.assertEqual(table.number, 2)
        table.add(3)
        self.assertEqual(table.number, 5)
        self.assertIn("Table", str(table))

    def test_thing_rejects_negative_number(self):
        with self.assertRaises(ValueError):
            Thing(number=-5)


if __name__ == "__main__":
    unittest.main()
