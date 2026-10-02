"""Baked-good service."""

from src.models.baked_good import BakedGood
from src.repositories.baked_good_repository import BakedGoodRepository


class BakedGoodService:
    def __init__(self, repository: BakedGoodRepository):
        self._repository = repository

    def create_baked_good(self, baked_good: BakedGood):
        pass

    def get_baked_goods(self):
        pass
