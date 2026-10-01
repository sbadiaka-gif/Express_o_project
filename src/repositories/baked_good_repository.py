"""Baked-good repository."""

from src.models.baked_good import BakedGood
from copy import deepcopy


class BakedGoodRepository:
    def __init__(self):
        self._baked_goods: list[BakedGood] = []
        self._next_id: int = 1

    def add(self, baked_good: BakedGood) -> BakedGood:
        baked_good.id = self._next_id
        self._next_id += 1
        self._baked_goods.append(deepcopy(baked_good))
        return baked_good

    def get_by_id(self, baked_good_id: int) -> BakedGood | None:
        for baked_good in self._baked_goods:
            if baked_good.id == baked_good_id:
                return deepcopy(baked_good)

        return None

    def get_all(self) -> list[BakedGood]:
        return deepcopy(self._baked_goods)

    def update(
        self, baked_good_id: int, updated_baked_good: BakedGood
    ) -> BakedGood | None:
        for index, BakedGood in enumerate(self._baked_goods):
            if BakedGood.id == baked_good_id:
                self._baked_goods[index] = deepcopy(updated_baked_good)
                return updated_baked_good

        return None

    def delete(self, baked_good_id: int) -> bool:
        for index, BakedGood in enumerate(self._baked_goods):
            if BakedGood.id == baked_good_id:
                del self._baked_goods[index]
                return True

        return False
