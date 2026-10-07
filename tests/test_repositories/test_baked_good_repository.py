# pyright: reportPrivateUsage = false

from decimal import Decimal

from src.models.baked_good import BakedGood
from src.repositories.baked_good_repository import BakedGoodRepository

baked_good_1 = BakedGood(
    "Sourdough Loaf",
    Decimal("3.20"),
    Decimal("120.00"),
    "Hearthstone Mill",
    ["Wheat", "Gluten"],
    Decimal("7.04"),
)

baked_good_2 = BakedGood(
    "Butter Croissant",
    Decimal("1.15"),
    Decimal("160.00"),
    "Golden Valley Dairy",
    ["Wheat", "Milk", "Eggs"],
    Decimal("2.99"),
)

baked_good_3 = BakedGood(
    "Blueberry Muffin",
    Decimal("1.40"),
    Decimal("150.00"),
    "Sunrise Bakery Supply",
    ["Wheat", "Milk", "Eggs"],
    Decimal("3.50"),
)

baked_good_4 = BakedGood(
    "Almond Biscotti",
    Decimal("0.85"),
    Decimal("200.00"),
    "Orchard Lane Nuts",
    ["Almonds", "Wheat", "Eggs"],
    Decimal("2.55"),
)

baked_good_5 = BakedGood(
    "Fudge Brownie",
    Decimal("1.80"),
    Decimal("105.00"),
    "Prairie Cocoa Co.",
    ["Eggs", "Milk", "Soy"],
    Decimal("3.69"),
)


def test_add_returns_object():
    test_repository = BakedGoodRepository()
    assert test_repository.add(baked_good_1) == baked_good_1


def test_add_saves_object():
    test_repository = BakedGoodRepository()
    test_repository.add(baked_good_1)
    assert test_repository._baked_goods[0] == baked_good_1


def test_get_by_id_gets():
    test_repository = BakedGoodRepository()
    baked_good_1.id = 1
    test_repository._baked_goods.append(baked_good_1)
    assert test_repository.get_by_id(1)


def test_get_by_id_gets_none_when_no_items():
    test_repository = BakedGoodRepository()
    assert not test_repository.get_by_id(1)


def test_get_by_id_gets_none_when_id_missing():
    test_repository = BakedGoodRepository()
    baked_good_1.id = 1
    test_repository._baked_goods.append(baked_good_1)
    assert not test_repository.get_by_id(0)


def test_get_all_gets_none_when_no_items():
    test_repository = BakedGoodRepository()
    assert test_repository.get_all() == []


def test_get_all_gets_all():
    test_repository = BakedGoodRepository()
    test_repository._baked_goods.append(baked_good_1)
    test_repository._baked_goods.append(baked_good_2)
    assert test_repository.get_all()


def test_update_returns_item():
    test_repository = BakedGoodRepository()
    baked_good_1.id = 1
    test_repository._baked_goods.append(baked_good_1)
    baked_good_2.id = 2
    test_repository._baked_goods.append(baked_good_2)
    assert test_repository.update(2, baked_good_3) == baked_good_3


def test_update_returns_none_missing_id():
    test_repository = BakedGoodRepository()
    assert not test_repository.update(1, baked_good_1)


def test_update_updates_item():
    test_repository = BakedGoodRepository()
    baked_good_1.id = 1
    test_repository._baked_goods.append(baked_good_1)
    baked_good_2.id = 2
    test_repository._baked_goods.append(baked_good_2)
    test_repository.update(2, baked_good_3)
    assert test_repository._baked_goods[1] == baked_good_3


def test_delete_returns_true_on_remove():
    test_repository = BakedGoodRepository()
    baked_good_1.id = 1
    test_repository._baked_goods.append(baked_good_1)
    baked_good_2.id = 2
    test_repository._baked_goods.append(baked_good_2)
    assert test_repository.delete(1)


def test_delete_returns_false_on_not_remove():
    test_repository = BakedGoodRepository()
    assert not test_repository.delete(1)


def test_delete_removes_item():
    test_repository = BakedGoodRepository()
    baked_good_1.id = 1
    test_repository._baked_goods.append(baked_good_1)
    baked_good_2.id = 2
    test_repository._baked_goods.append(baked_good_2)
    test_repository.delete(2)
    assert len(test_repository._baked_goods) == 1
