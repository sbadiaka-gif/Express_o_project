# pyright: reportPrivateUsage = false

from decimal import Decimal
from pytest_mock import MockerFixture
from pytest import raises

from src.models.baked_good import BakedGood
from src.services.baked_good_service import BakedGoodService
from src.repositories.baked_good_repository import BakedGoodRepository
from src.exceptions import BakedGoodDuplicateItemError, BakedGoodNotFoundError

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


def test_create_baked_good_calls_add(mocker: MockerFixture):
    test_repository = BakedGoodRepository()
    mock_add = mocker.patch.object(test_repository, "add")

    test_service = BakedGoodService(test_repository)
    mocker.patch.object(test_service, "_validate_baked_good")
    mocker.patch.object(test_service, "_validate_is_unique")
    test_service.create_baked_good(baked_good_1)

    mock_add.assert_called_once_with(baked_good_1)


def test_create_baked_good_returns_value(mocker: MockerFixture):
    test_repository = BakedGoodRepository()
    mock_add = mocker.patch.object(test_repository, "add")
    mock_add.return_value = "Test Value"

    test_service = BakedGoodService(test_repository)
    mocker.patch.object(test_service, "_validate_baked_good")
    mocker.patch.object(test_service, "_validate_is_unique")

    assert test_service.create_baked_good(baked_good_1) == "Test Value"


def test_get_baked_goods(mocker: MockerFixture):
    test_repository = BakedGoodRepository()
    mock_get_all = mocker.patch.object(test_repository, "get_all")
    mock_get_all.return_value = "Test Value"

    test_service = BakedGoodService(test_repository)
    assert test_service.get_baked_goods() == "Test Value"


def test_get_baked_good_call_get_by_id(mocker: MockerFixture):
    test_repository = BakedGoodRepository()
    mock_get_by_id = mocker.patch.object(test_repository, "get_by_id")

    test_service = BakedGoodService(test_repository)
    mocker.patch.object(test_service, "_validate_baked_good_exists")

    test_service.get_baked_good(1)
    mock_get_by_id.assert_called_once_with(1)


def test_get_baked_good_returns_value(mocker: MockerFixture):
    test_repository = BakedGoodRepository()
    mock_get_by_id = mocker.patch.object(test_repository, "get_by_id")
    mock_get_by_id.return_value = "Test Value"

    test_service = BakedGoodService(test_repository)
    mocker.patch.object(test_service, "_validate_baked_good_exists")

    assert test_service.get_baked_good(1) == "Test Value"


def test_get_baked_good_by_id_call_get_by_id(mocker: MockerFixture):
    test_repository = BakedGoodRepository()
    mock_get_by_id = mocker.patch.object(test_repository, "get_by_id")

    test_service = BakedGoodService(test_repository)

    test_service.get_baked_good_by_id(1)
    mock_get_by_id.assert_called_once_with(1)


def test_get_baked_good_by_id_returns_value(mocker: MockerFixture):
    test_repository = BakedGoodRepository()
    mock_get_by_id = mocker.patch.object(test_repository, "get_by_id")
    mock_get_by_id.return_value = "Test Value"

    test_service = BakedGoodService(test_repository)

    assert test_service.get_baked_good_by_id(1) == "Test Value"


def test_update_baked_good_calls_update(mocker: MockerFixture):
    test_repository = BakedGoodRepository()
    mock_update = mocker.patch.object(test_repository, "update")
    mock_update.return_value = "Test Value"

    test_service = BakedGoodService(test_repository)
    mocker.patch.object(test_service, "_validate_baked_good_exists")
    mocker.patch.object(test_service, "_validate_baked_good")
    mocker.patch.object(test_service, "_validate_is_unique")

    test_service.update_baked_good(1, baked_good_1)

    mock_update.assert_called_once_with(1, baked_good_1)


def test_update_baked_good_returns_value(mocker: MockerFixture):
    test_repository = BakedGoodRepository()
    mock_update = mocker.patch.object(test_repository, "update")
    mock_update.return_value = baked_good_1

    test_service = BakedGoodService(test_repository)
    mocker.patch.object(test_service, "_validate_baked_good_exists")
    mocker.patch.object(test_service, "_validate_baked_good")
    mocker.patch.object(test_service, "_validate_is_unique")

    assert test_service.update_baked_good(1, baked_good_1) == baked_good_1


def test_remove_baked_good_calls_delete(mocker: MockerFixture):
    test_repository = BakedGoodRepository()
    mock_delete = mocker.patch.object(test_repository, "delete")

    test_service = BakedGoodService(test_repository)
    mocker.patch.object(test_service, "_validate_baked_good_exists")

    test_service.remove_baked_good(1)

    mock_delete.assert_called_once_with(1)


def test_validate_baked_good_passes(mocker: MockerFixture):
    test_repository = BakedGoodRepository()

    mocker.patch("src.validators.validate_name_not_empty")
    mocker.patch("src.validators.validate_money_decimal_positive_two_decimal_places")
    mocker.patch("src.validators.validate_markup_is_decimal_and_positive")
    test_service = BakedGoodService(test_repository)
    mocker.patch.object(test_service, "_validate_allergens")

    test_service._validate_baked_good(baked_good_1)


def test_validate_baked_good_exists_calls_get_by_id(mocker: MockerFixture):
    test_repository = BakedGoodRepository()
    mock_get_by_id = mocker.patch.object(test_repository, "get_by_id")
    test_service = BakedGoodService(test_repository)

    test_service._validate_baked_good_exists(1)

    mock_get_by_id.assert_called_once_with(1)


def test_validate_baked_good_exists_errors_on_not_found(mocker: MockerFixture):
    test_repository = BakedGoodRepository()
    mock_get_by_id = mocker.patch.object(test_repository, "get_by_id")
    mock_get_by_id.return_value = None

    test_service = BakedGoodService(test_repository)

    with raises(BakedGoodNotFoundError):
        test_service._validate_baked_good_exists(1)


def test_validate_baked_good_exists_passes_when_found(mocker: MockerFixture):
    test_repository = BakedGoodRepository()
    mock_get_by_id = mocker.patch.object(test_repository, "get_by_id")
    mock_get_by_id.return_value = baked_good_1

    test_service = BakedGoodService(test_repository)

    test_service._validate_baked_good_exists(1)


def test_validate_allergens_full_list(mocker: MockerFixture):
    test_repository = BakedGoodRepository()
    test_service = BakedGoodService(test_repository)

    mocker.patch("src.validators.validate_name_not_empty")

    test_service._validate_allergens(["Wheat", "Eggs"])


def test_validate_allergens__empty_list(mocker: MockerFixture):
    test_repository = BakedGoodRepository()
    test_service = BakedGoodService(test_repository)

    mocker.patch("src.validators.validate_name_not_empty")

    test_service._validate_allergens([])


def test_validate_is_unique_calls_get_all(mocker: MockerFixture):
    test_repository = BakedGoodRepository()
    mock_get_all = mocker.patch.object(test_repository, "get_all")
    mock_get_all.return_value = []

    test_service = BakedGoodService(test_repository)
    test_service._validate_is_unique(baked_good_1)

    mock_get_all.assert_called_once()


def test_validate_is_unique_raises_error_on_found(mocker: MockerFixture):
    test_repository = BakedGoodRepository()
    mock_get_all = mocker.patch.object(test_repository, "get_all")
    mock_get_all.return_value = [baked_good_1, baked_good_2]

    test_service = BakedGoodService(test_repository)
    with raises(BakedGoodDuplicateItemError):
        test_service._validate_is_unique(baked_good_2)


def test_validate_is_unique_passes_on_not_found(mocker: MockerFixture):
    test_repository = BakedGoodRepository()
    mock_get_all = mocker.patch.object(test_repository, "get_all")
    mock_get_all.return_value = [baked_good_1, baked_good_2]

    test_service = BakedGoodService(test_repository)
    test_service._validate_is_unique(baked_good_3)
