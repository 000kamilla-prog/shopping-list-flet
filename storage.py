from abc import ABC, abstractmethod


class BaseStorage(ABC):
    @abstractmethod
    def set(self, key, value):
        pass

    @abstractmethod
    def get(self, key):
        pass


class PairStorage(BaseStorage):
    def __init__(self):
        self.pairs = []

    @property
    def pairs(self):
        return self._pairs.copy()

    @pairs.setter
    def pairs(self, value):
        self._pairs = list(value)

    def set(self, key, value):
        for index, pair in enumerate(self._pairs):
            if pair[0] == key:
                self._pairs[index] = (key, value)
                return
        self._pairs.append((key, value))

    def get(self, key):
        for pair in self._pairs:
            if pair[0] == key:
                return pair[1]
        return None

    def __str__(self):
        return f"Записей: {len(self._pairs)}"

    def __repr__(self):
        return f"PairStorage({self._pairs!r})"

    def __eq__(self, other):
        if not isinstance(other, PairStorage):
            return NotImplemented
        return self._pairs == other._pairs

    def __len__(self):
        return len(self._pairs)

    def __contains__(self, key):
        return any(pair[0] == key for pair in self._pairs)

    def __iter__(self):
        return iter(self._pairs)
