"""Baked-good service."""

from src.models.baked_good import BakedGood
from src.repositories.baked_good_repository import BakedGoodRepository
from validators import (
    validate_money_decimal_positive_two_decimal_places,
    validate_name_not_empty,
    validate_markup_is_decimal_and_positive,
)
from exceptions import BakedGoodNotFoundError, BakedGoodDuplicateItemError
from typing import cast


class BakedGoodService:
    def __init__(self, repository: BakedGoodRepository):
        self._repository = repository

    def create_baked_good(self, baked_good: BakedGood) -> BakedGood:
        self.validate_baked_good(baked_good)
        self.validate_is_unique(baked_good)

        return self._repository.add(baked_good)

    def get_baked_good(self, id: int) -> BakedGood:
        self.validate_baked_good_exists(id)
        return cast(BakedGood, self._repository.get_by_id(id))

    def update_baked_good(self, id: int, baked_good: BakedGood) -> BakedGood:
        self.validate_baked_good_exists(id)
        self.validate_baked_good(baked_good)
        self.validate_is_unique(baked_good)

        return cast(BakedGood, self._repository.update(id, baked_good))

    def remove_baked_good(self, id: int):
        self.validate_baked_good_exists(id)
        self._repository.delete(id)

    def validate_baked_good(self, baked_good: BakedGood):
        validate_name_not_empty(baked_good.name, "name")
        validate_money_decimal_positive_two_decimal_places(
            baked_good.purchasing_cost, "purchasing_cost"
        )
        validate_markup_is_decimal_and_positive(baked_good.markup_percentage)
        self.validate_allergens(baked_good.allergens)
        validate_name_not_empty(baked_good.vendor_name, "vendor_name")

    def validate_baked_good_exists(self, id: int):
        baked_good = self._repository.get_by_id(id)
        if baked_good == None:
            raise BakedGoodNotFoundError(f"Baked good by id '{int}' not found.")

    def validate_allergens(self, allergens: list[str]):
        for allergen in allergens:
            validate_name_not_empty(allergen, "allergen")

    def validate_is_unique(self, new_baked_good: BakedGood):
        for baked_good in self._repository.get_all():
            if (
                baked_good.name == new_baked_good.name
                and baked_good.allergens == new_baked_good.allergens
                and baked_good.markup_percentage == new_baked_good.markup_percentage
                and baked_good.purchasing_cost == new_baked_good.purchasing_cost
                and baked_good.vendor_name == new_baked_good.vendor_name
                and baked_good.sale_price == new_baked_good.sale_price
            ):
                raise BakedGoodDuplicateItemError(
                    f"Baked good '{new_baked_good}' already exists."
                )
