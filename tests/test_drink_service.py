from decimal import Decimal

import pytest

from src.exceptions import IngredientNotFoundError
from src.models.drink import Drink
from src.models.ingredient import Ingredient
from src.models.recipe_item import RecipeItem
from src.repositories.drink_repository import DrinkRepository
from src.repositories.ingredient_repository import IngredientRepository
from src.services.drink_service import DrinkService
from src.services.ingredient_service import IngredientService


def make_drink(name="Latte", recipe=None):
    return Drink(
        name=name,
        recipe=recipe or [],
        markup_percentage=Decimal("0.50"),
        cost_to_produce=Decimal("2.00"),
        sale_price=Decimal("3.00"),
    )


class TestDrinkService:
    @pytest.fixture
    def setup(self):
        ingredient_repo = IngredientRepository()
        ingredient_service = IngredientService(ingredient_repo)
        service = DrinkService(DrinkRepository(), ingredient_service)

        milk = ingredient_repo.add(
            Ingredient(
                name="Milk",
                purchasing_cost=Decimal("1.00"),
                unit_amount=Decimal("10.00"),
                unit_of_measure="kg",
            )
        )
        espresso = ingredient_repo.add(
            Ingredient(
                name="Espresso",
                purchasing_cost=Decimal("2.00"),
                unit_amount=Decimal("5.00"),
                unit_of_measure="kg",
            )
        )
        return {
            "service": service,
            "ingredients": ingredient_repo,
            "milk_id": milk.id,
            "espresso_id": espresso.id,
        }

    # add_drink / get_by_id

    def test_add_drink_assigns_id_and_stores(self, setup):
        drink = setup["service"].add_drink(make_drink())

        assert drink.id is not None
        assert setup["service"].get_by_id(drink.id).name == "Latte"

    def test_get_by_id_unknown_returns_none(self, setup):
        assert setup["service"].get_by_id(999) is None

    def test_add_drink_duplicate_name_raises(self, setup):
        setup["service"].add_drink(make_drink())
        with pytest.raises(Exception):  # swap for the validator's exact type
            setup["service"].add_drink(make_drink())

    def test_add_drink_empty_name_raises(self, setup):
        with pytest.raises(Exception):  # swap for the validator's exact type
            setup["service"].add_drink(make_drink(name=""))

    def test_add_drink_negative_price_raises(self, setup):
        bad = make_drink()
        bad.sale_price = Decimal("-1.00")
        with pytest.raises(ValueError):
            setup["service"].add_drink(bad)

    # price, markup, cost

    def test_change_drink_price(self, setup):
        drink = setup["service"].add_drink(make_drink())
        setup["service"].change_drink_price(drink.id, Decimal("4.50"))

        assert setup["service"].get_by_id(drink.id).sale_price == Decimal("4.50")

    def test_change_drink_markup(self, setup):
        drink = setup["service"].add_drink(make_drink())
        setup["service"].change_drink_markup(drink.id, Decimal("0.75"))

        assert setup["service"].get_by_id(drink.id).markup_percentage == Decimal("0.75")

    def test_change_cost_to_produce(self, setup):
        drink = setup["service"].add_drink(make_drink())
        setup["service"].change_cost_to_produce(drink.id, Decimal("2.50"))

        assert setup["service"].get_by_id(drink.id).cost_to_produce == Decimal("2.50")

    def test_change_price_too_many_decimals_raises(self, setup):
        drink = setup["service"].add_drink(make_drink())
        with pytest.raises(ValueError):
            setup["service"].change_drink_price(drink.id, Decimal("1.999"))

    def test_change_price_unknown_drink_raises(self, setup):
        with pytest.raises(Exception):  # swap for validate_record_exists' type
            setup["service"].change_drink_price(999, Decimal("4.00"))

    # recipe editing

    def test_change_drink_recipe_replaces_recipe(self, setup):
        drink = setup["service"].add_drink(
            make_drink(recipe=[RecipeItem(ingredient_id=setup["milk_id"], quantity=Decimal("2.00"))])
        )
        new_recipe = [RecipeItem(ingredient_id=setup["espresso_id"], quantity=Decimal("1.00"))]
        setup["service"].change_drink_recipe(drink.id, new_recipe)

        recipe = setup["service"].get_by_id(drink.id).recipe
        assert [item.ingredient_id for item in recipe] == [setup["espresso_id"]]

    def test_change_drink_recipe_unknown_ingredient_raises(self, setup):
        drink = setup["service"].add_drink(make_drink())
        with pytest.raises(Exception):  # swap for validate_record_exists' type
            setup["service"].change_drink_recipe(
                drink.id, [RecipeItem(ingredient_id=999, quantity=Decimal("1.00"))]
            )

    def test_add_to_drink_recipe_appends(self, setup):
        drink = setup["service"].add_drink(make_drink())
        setup["service"].add_to_drink_recipe(
            drink.id, RecipeItem(ingredient_id=setup["milk_id"], quantity=Decimal("2.00"))
        )

        recipe = setup["service"].get_by_id(drink.id).recipe
        assert len(recipe) == 1
        assert recipe[0].quantity == Decimal("2.00")

    def test_add_recipe_items_adds_several(self, setup):
        drink = setup["service"].add_drink(make_drink())
        setup["service"].add_recipe_items(
            drink.id,
            [
                RecipeItem(ingredient_id=setup["milk_id"], quantity=Decimal("2.00")),
                RecipeItem(ingredient_id=setup["espresso_id"], quantity=Decimal("1.00")),
            ],
        )

        assert len(setup["service"].get_by_id(drink.id).recipe) == 2

    def test_remove_from_drink_recipe(self, setup):
        drink = setup["service"].add_drink(
            make_drink(
                recipe=[
                    RecipeItem(ingredient_id=setup["milk_id"], quantity=Decimal("2.00")),
                    RecipeItem(ingredient_id=setup["espresso_id"], quantity=Decimal("1.00")),
                ]
            )
        )
        setup["service"].remove_from_drink_recipe(drink.id, setup["milk_id"])

        recipe = setup["service"].get_by_id(drink.id).recipe
        assert [item.ingredient_id for item in recipe] == [setup["espresso_id"]]

    def test_remove_missing_ingredient_raises(self, setup):
        drink = setup["service"].add_drink(
            make_drink(recipe=[RecipeItem(ingredient_id=setup["milk_id"], quantity=Decimal("2.00"))])
        )
        with pytest.raises(IngredientNotFoundError):
            setup["service"].remove_from_drink_recipe(drink.id, setup["espresso_id"])

    def test_recipe_edits_do_not_change_stock(self, setup):
        drink = setup["service"].add_drink(make_drink())
        setup["service"].add_to_drink_recipe(
            drink.id, RecipeItem(ingredient_id=setup["milk_id"], quantity=Decimal("2.00"))
        )

        assert setup["ingredients"].get_by_id(setup["milk_id"]).unit_amount == Decimal("10.00")