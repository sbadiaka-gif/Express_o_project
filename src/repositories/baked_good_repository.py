from src.models.baked_good import BakedGood
from copy import deepcopy
from src.repositories.repository import Repository


class BakedGoodRepository(Repository[BakedGood]):
    def __init__(self):
        self._baked_goods: list[BakedGood] = []
        self._next_id: int = 1

    def add(self, item: BakedGood) -> BakedGood:
        """Add a new baked good to the data."""
        item.id = self._next_id
        self._next_id += 1
        self._baked_goods.append(deepcopy(item))
        return item

    def get_by_id(self, id: int) -> BakedGood | None:
        """Get a baked good with the id."""
        for baked_good in self._baked_goods:
            if baked_good.id == id:
                return deepcopy(baked_good)
        return None

    def get_all(self) -> list[BakedGood]:
        """Get the list of baked goods."""
        return deepcopy(self._baked_goods)

    def update(self, id: int, updated_item: BakedGood) -> BakedGood | None:
        """Replace a baked good with the id."""
        for index, BakedGood in enumerate(self._baked_goods):
            if BakedGood.id == id:
                self._baked_goods[index] = deepcopy(updated_item)
                return updated_item
        return None

    def delete(self, id: int) -> bool:
        """Remove a baked good with the id."""
        for index, BakedGood in enumerate(self._baked_goods):
            if BakedGood.id == id:
                del self._baked_goods[index]
                return True
        return False
