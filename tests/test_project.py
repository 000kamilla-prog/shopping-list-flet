import ast
import unittest
from pathlib import Path

from models import Item, BaseItem
from storage import PairStorage, BaseStorage


ROOT = Path(__file__).resolve().parents[1]


class ItemTests(unittest.TestCase):
    def test_inheritance_and_properties(self):
        item = Item(" Молоко ")
        self.assertIsInstance(item, BaseItem)
        self.assertEqual(item.name, "Молоко")
        item.bought = True
        self.assertTrue(item.bought)
        item.name = "Чай"
        self.assertEqual(item.get_name(), "Чай")

    def test_empty_name_is_not_allowed(self):
        with self.assertRaises(ValueError):
            Item("  ")

    def test_comparison_and_special_methods(self):
        self.assertEqual(Item("ХЛЕБ"), Item("хлеб"))
        self.assertLess(Item("А"), Item("Б"))
        self.assertGreater(Item("Я"), Item("Б"))
        self.assertTrue(Item("А") <= Item("А"))
        self.assertEqual(str(Item("Чай")), "Чай")
        self.assertIn("Item(", repr(Item("Чай")))


class StorageTests(unittest.TestCase):
    def test_storage_without_dict(self):
        store = PairStorage()
        self.assertIsInstance(store, BaseStorage)
        store.set("login", "student")
        store.set("login", "new_student")
        self.assertEqual(store.get("login"), "new_student")
        self.assertEqual(len(store), 1)
        self.assertIn("login", store)
        self.assertEqual(list(store), [("login", "new_student")])
        self.assertIsNone(store.get("unknown"))

    def test_storage_properties(self):
        store = PairStorage()
        store.pairs = [("a", 1)]
        self.assertEqual(store.pairs, [("a", 1)])
        copy = store.pairs
        copy.clear()
        self.assertEqual(len(store), 1)


class RequirementsTests(unittest.TestCase):
    def test_ten_custom_controls(self):
        tree = ast.parse((ROOT / "components.py").read_text(encoding="utf-8"))
        components = [
            node for node in tree.body
            if isinstance(node, ast.ClassDef)
            and any(isinstance(deco, ast.Attribute) and deco.attr == "control"
                    for deco in node.decorator_list)
        ]
        self.assertEqual(len(components), 10)

    def test_no_builtin_dict_in_project_code(self):
        for path in ROOT.glob("*.py"):
            tree = ast.parse(path.read_text(encoding="utf-8"))
            self.assertFalse(any(isinstance(node, ast.Dict) for node in ast.walk(tree)), path.name)
            self.assertFalse(any(
                isinstance(node, ast.Call) and isinstance(node.func, ast.Name)
                and node.func.id == "dict" for node in ast.walk(tree)
            ), path.name)


if __name__ == "__main__":
    unittest.main()
