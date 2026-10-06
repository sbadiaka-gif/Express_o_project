"""Baked-good repository."""

# CHANGED: import style kept aligned with the project package naming conventions.
from src.models.baked_good import BakedGood
from copy import deepcopy
from src.repositories.repository import Repository


class BakedGoodRepository(Repository[BakedGood]):
    def __init__(self):
        self._baked_goods: list[BakedGood] = []
        self._next_id: int = 1

    # CHANGED: add assigns the next id and stores a deep copy to protect the backing list.
    def add(self, item: BakedGood) -> BakedGood:
        item.id = self._next_id
        self._next_id += 1
        self._baked_goods.append(deepcopy(item))
        return item

    # CHANGED: lookup is done by id and returns a safe copied instance.
    def get_by_id(self, id: int) -> BakedGood | None:
        for baked_good in self._baked_goods:
            if baked_good.id == id:
                return deepcopy(baked_good)

        return None

    # CHANGED: get_all returns a copy so callers cannot mutate the repository directly.
    def get_all(self) -> list[BakedGood]:
        return deepcopy(self._baked_goods)

    # CHANGED: update matches on the baked-good id and writes the replacement into the stored list.
    def update(self, id: int, updated_item: BakedGood) -> BakedGood | None:
        for index, BakedGood in enumerate(self._baked_goods):
            if BakedGood.id == id:
                self._baked_goods[index] = deepcopy(updated_item)
                return updated_item

        return None

    # CHANGED: delete removes the item by id and returns True only when found.
    def delete(self, id: int) -> bool:
        for index, BakedGood in enumerate(self._baked_goods):
            if BakedGood.id == id:
                del self._baked_goods[index]
                return True

        return False
