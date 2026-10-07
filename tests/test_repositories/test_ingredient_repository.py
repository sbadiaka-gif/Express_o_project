from decimal import Decimal

import pytest

from src.models.ingredient import Ingredient
from src.repositories.ingredient_repository import IngredientRepository


def make_ingredient(name="Milk"):
    return Ingredient(
        name=name,
        purchasing_cost=Decimal("1.00"),
        unit_amount=Decimal("10.00"),
        unit_of_measure="kg",
    )


@pytest.fixture
def repo():
    return IngredientRepository()


def test_add_assigns_sequential_ids(repo):
    first = repo.add(make_ingredient("Milk"))
    second = repo.add(make_ingredient("Sugar"))

    assert first.id == 1
    assert second.id == 2


def test_get_by_id_returns_stored_ingredient(repo):
    ingredient = repo.add(make_ingredient())

    assert repo.get_by_id(ingredient.id).name == "Milk"


def test_get_by_id_unknown_returns_none(repo):
    assert repo.get_by_id(999) is None


def test_get_all_returns_every_ingredient(repo):
    repo.add(make_ingredient("Milk"))
    repo.add(make_ingredient("Sugar"))

    assert [i.name for i in repo.get_all()] == ["Milk", "Sugar"]


def test_get_all_empty(repo):
    assert repo.get_all() == []


def test_add_stores_a_copy(repo):
    ingredient = make_ingredient()
    repo.add(ingredient)
    ingredient.unit_amount = Decimal("99.00")

    assert repo.get_by_id(ingredient.id).unit_amount == Decimal("10.00")


def test_get_by_id_returns_a_copy(repo):
    ingredient = repo.add(make_ingredient())
    fetched = repo.get_by_id(ingredient.id)
    fetched.unit_amount = Decimal("99.00")

    assert repo.get_by_id(ingredient.id).unit_amount == Decimal("10.00")


def test_get_all_returns_copies(repo):
    repo.add(make_ingredient())
    repo.get_all()[0].unit_amount = Decimal("99.00")

    assert repo.get_all()[0].unit_amount == Decimal("10.00")


def test_update_replaces_ingredient(repo):
    ingredient = repo.add(make_ingredient())
    changed = make_ingredient("Oat Milk")
    changed.id = ingredient.id

    result = repo.update(ingredient.id, changed)

    assert result.name == "Oat Milk"
    assert repo.get_by_id(ingredient.id).name == "Oat Milk"


def test_update_unknown_returns_none(repo):
    assert repo.update(999, make_ingredient()) is None


def test_delete_removes_ingredient(repo):
    ingredient = repo.add(make_ingredient())

    assert repo.delete(ingredient.id) is True
    assert repo.get_by_id(ingredient.id) is None


def test_delete_unknown_returns_false(repo):
    assert repo.delete(999) is False


def test_ids_are_not_reused_after_delete(repo):
    first = repo.add(make_ingredient("Milk"))
    repo.delete(first.id)
    second = repo.add(make_ingredient("Sugar"))

    assert second.id == 2