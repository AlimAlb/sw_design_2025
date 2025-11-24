import os
import sys
import unittest
from typing import Tuple, cast

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from animal_classes import Monkey
from di_container import di_container
from inventory_classes import Table
from vet_clinic import Vetclinic


class DIContainerTests(unittest.TestCase):
    def test_singleton_resolves_same_instance_and_accumulates_items(self):
        container = di_container()
        container.register(Table, singleton=True)

        first = cast(Table, container.resolve(Table, number=1))
        second = cast(Table, container.resolve(Table, number=3))

        self.assertIs(first, second)
        self.assertEqual(first.number, 4)

    def test_scoped_resolution_runs_vetclinic_check(self):
        container = di_container()
        container.register(Vetclinic, singleton=True)
        container.register(Monkey, singleton=False)

        container.resolve(Vetclinic, func=lambda x: False)
        accepted, obj = cast(
            Tuple[bool, Monkey],
            container.resolve(Monkey, food=2, is_healthy=True, wellness=6),
        )
        self.assertFalse(accepted)
        self.assertIsInstance(obj, Monkey)

        container = di_container()
        container.register(Vetclinic, singleton=True)
        container.register(Monkey, singleton=False)
        container.resolve(Vetclinic, func=lambda x: True)
        accepted, obj = cast(
            Tuple[bool, Monkey],
            container.resolve(Monkey, food=1, is_healthy=True, wellness=9),
        )
        self.assertTrue(accepted)
        self.assertIsInstance(obj, Monkey)

    def test_resolve_unregistered_raises_key_error(self):
        container = di_container()
        with self.assertRaises(KeyError):
            container.resolve(Table)


if __name__ == "__main__":
    unittest.main()
