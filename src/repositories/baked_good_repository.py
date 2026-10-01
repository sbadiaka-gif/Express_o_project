"""Baked-good repository."""
from src.models.baked_good import BakedGood
from copy import deepcopy

class BakedGoodRepository:
    def __init__(self):
        self._BakedGoods: list[BakedGood] = []
        self._next_id: int = 1

    def add(self, BakedGood: BakedGood) -> BakedGood:
        BakedGood.id = self._next_id
        self._next_id += 1
        self._BakedGoods.append(BakedGood)
        return deepcopy(BakedGood)
    
    def get_by_id(self, BakedGood_id: int) -> BakedGood | None:
        for BakedGood in self._BakedGoods:
            if BakedGood.id == BakedGood_id:
                return deepcopy(BakedGood)
        
        return None
    
    def get_all(self) -> list[BakedGood]:
        return deepcopy(self._BakedGoods)
    
    def update(self, updated_BakedGood: BakedGood) -> BakedGood | None:
        for index, BakedGood in enumerate(self._BakedGoods):
            if BakedGood.id == updated_BakedGood.id:
                self._BakedGoods[index] = updated_BakedGood
                return deepcopy(updated_BakedGood)
        
        return None
    
    def delete(self, BakedGood_id: int) -> bool:
        for index, BakedGood in enumerate(self._BakedGoods):
            if BakedGood.id == BakedGood_id:
                del self._BakedGoods[index]
                return True
        
        return False