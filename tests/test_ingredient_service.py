from decimal import Decimal

import pytest

from src.exceptions import InsufficientStockError
from src.models.ingredient import Ingredient
from src.repositories.ingredient_repository import IngredientRepository
from src.services.ingredient_service import IngredientService


class TestIngredientService:
    @pytest.fixture
    def setup(self):
        repo = IngredientRepository()
        service = IngredientService(repo)
        milk = repo.add(
            Ingredient(
                name="Milk",
                purchasing_cost=Decimal("1.00"),
                unit_amount=Decimal("10.00"),
                unit_of_measure="kg",
            )
        )
        return {"service": service, "repo": repo, "milk_id": milk.id}

    # restock

    def test_restock_increases_amount(self, setup):
        setup["service"].restock_ingredient(setup["milk_id"], Decimal("5.00"))

        assert setup["repo"].get_by_id(setup["milk_id"]).unit_amount == Decimal("15.00")

    def test_restock_unknown_ingredient_raises(self, setup):
        with pytest.raises(Exception):  # swap for validate_record_exists' type
            setup["service"].restock_ingredient(999, Decimal("5.00"))

    def test_restock_too_many_decimals_raises(self, setup):
        with pytest.raises(ValueError):
            setup["service"].restock_ingredient(setup["milk_id"], Decimal("1.999"))

    def test_restock_negative_amount_raises(self, setup):
        with pytest.raises(ValueError):
            setup["service"].restock_ingredient(setup["milk_id"], Decimal("-1.00"))

    def test_restock_float_raises(self, setup):
        with pytest.raises(ValueError):
            setup["service"].restock_ingredient(setup["milk_id"], 5.0)

    # sufficient check

    def test_sufficient_when_enough(self, setup):
        assert setup["service"].is_ingredient_amount_sufficient(
            setup["milk_id"], Decimal("10.00")
        ) is True

    def test_not_sufficient_when_too_little(self, setup):
        assert setup["service"].is_ingredient_amount_sufficient(
            setup["milk_id"], Decimal("10.01")
        ) is False

    def test_sufficient_check_does_not_change_stock(self, setup):
        setup["service"].is_ingredient_amount_sufficient(setup["milk_id"], Decimal("3.00"))

        assert setup["repo"].get_by_id(setup["milk_id"]).unit_amount == Decimal("10.00")

    def test_sufficient_unknown_ingredient_raises(self, setup):
        with pytest.raises(Exception):  # swap for validate_record_exists' type
            setup["service"].is_ingredient_amount_sufficient(999, Decimal("1.00"))

    # deduct

    def test_deduct_decreases_amount(self, setup):
        setup["service"].deduct_ingredient_amount(setup["milk_id"], Decimal("4.00"))

        assert setup["repo"].get_by_id(setup["milk_id"]).unit_amount == Decimal("6.00")

    def test_deduct_exact_amount_reaches_zero(self, setup):
        setup["service"].deduct_ingredient_amount(setup["milk_id"], Decimal("10.00"))

        assert setup["repo"].get_by_id(setup["milk_id"]).unit_amount == Decimal("0.00")

    def test_deduct_more_than_available_raises_and_changes_nothing(self, setup):
        with pytest.raises(InsufficientStockError):
            setup["service"].deduct_ingredient_amount(setup["milk_id"], Decimal("10.01"))

        assert setup["repo"].get_by_id(setup["milk_id"]).unit_amount == Decimal("10.00")

    def test_deduct_unknown_ingredient_raises(self, setup):
        with pytest.raises(Exception):  # swap for validate_record_exists' type
            setup["service"].deduct_ingredient_amount(999, Decimal("1.00"))

    # exists

    def test_validate_ingredient_exists_passes(self, setup):
        assert setup["service"].validate_ingredient_exists(setup["milk_id"]) is None

    def test_validate_ingredient_exists_unknown_raises(self, setup):
        with pytest.raises(Exception):  # swap for validate_record_exists' type
            setup["service"].validate_ingredient_exists(999)