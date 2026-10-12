from abc import ABC, abstractmethod


class BaseItem(ABC):
    @abstractmethod
    def get_name(self):
        pass


class Item(BaseItem):
    def __init__(self, name, bought=False):
        self.name = name
        self.bought = bought

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        value = value.strip()
        if not value:
            raise ValueError("Название товара не может быть пустым")
        self._name = value

    @property
    def bought(self):
        return self._bought

    @bought.setter
    def bought(self, value):
        self._bought = bool(value)

    def get_name(self):
        return self.name

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"Item({self.name!r}, {self.bought!r})"

    def __eq__(self, other):
        if not isinstance(other, Item):
            return NotImplemented
        return self.name.lower() == other.name.lower()

    def __lt__(self, other):
        if not isinstance(other, Item):
            return NotImplemented
        return self.name.lower() < other.name.lower()

    def __le__(self, other):
        if not isinstance(other, Item):
            return NotImplemented
        return self.name.lower() <= other.name.lower()

    def __gt__(self, other):
        if not isinstance(other, Item):
            return NotImplemented
        return self.name.lower() > other.name.lower()
