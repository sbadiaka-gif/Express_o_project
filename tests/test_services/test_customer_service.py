# pyright: reportPrivateUsage = false

from decimal import Decimal
from pytest_mock import MockerFixture
from pytest import raises

from src.models.customer import Customer
from src.services.customer_service import CustomerService
from src.repositories.customer_repository import CustomerRepository
from src.exceptions import CustomerNotFoundError, CustomerDuplicateEmailError

customer_1 = Customer(
    "Alice Johnson",
    "alice.johnson@example.com",
    Decimal("245.50"),
)

customer_2 = Customer(
    "Brian Smith",
    "brian.smith@example.com",
    Decimal("0.00"),
)

customer_3 = Customer(
    "Carla Gomez",
    "carla.gomez@example.com",
    Decimal("1020.00"),
)

customer_4 = Customer(
    "David Lee",
    "david.lee@example.com",
    Decimal("15.25"),
)

customer_5 = Customer(
    "Emma Wilson",
    "emma.wilson@example.com",
    Decimal("560.75"),
)


def test_create_customer_calls_add(mocker: MockerFixture):
    test_repository = CustomerRepository()
    mock_add = mocker.patch.object(test_repository, "add")

    test_service = CustomerService(test_repository)
    mocker.patch.object(test_service, "_validate_customer")
    mocker.patch.object(test_service, "_validate_email_unique")
    test_service.create_customer(customer_1)

    mock_add.assert_called_once_with(customer_1)


def test_create_customer_returns_value(mocker: MockerFixture):
    test_repository = CustomerRepository()
    mock_add = mocker.patch.object(test_repository, "add")
    mock_add.return_value = "Test Value"

    test_service = CustomerService(test_repository)
    mocker.patch.object(test_service, "_validate_customer")
    mocker.patch.object(test_service, "_validate_email_unique")

    assert test_service.create_customer(customer_1) == "Test Value"


def test_get_by_email_gets_customer_on_match(mocker: MockerFixture):
    test_repository = CustomerRepository()
    mock_get_all = mocker.patch.object(test_repository, "get_all")
    mock_get_all.return_value = [customer_1, customer_2]

    test_service = CustomerService(test_repository)
    assert test_service.get_by_email(customer_2.email) == customer_2


def test_get_by_email_gives_none_on_missing(mocker: MockerFixture):
    test_repository = CustomerRepository()
    mock_get_all = mocker.patch.object(test_repository, "get_all")
    mock_get_all.return_value = [customer_1, customer_2]

    test_service = CustomerService(test_repository)
    assert not test_service.get_by_email("test.missing@example.com")


def test_get_by_email_gives_none_on_empty_list(mocker: MockerFixture):
    test_repository = CustomerRepository()
    mock_get_all = mocker.patch.object(test_repository, "get_all")
    mock_get_all.return_value = []

    test_service = CustomerService(test_repository)
    assert not test_service.get_by_email("test.missing@example.com")


def test_get_customers_gets_customers(mocker: MockerFixture):
    test_repository = CustomerRepository()
    mock_get_all = mocker.patch.object(test_repository, "get_all")
    mock_get_all.return_value = "Test Value"

    test_service = CustomerService(test_repository)
    assert test_service.get_customers() == "Test Value"


def test_get_customer_call_get_by_id(mocker: MockerFixture):
    test_repository = CustomerRepository()
    mock_get_by_id = mocker.patch.object(test_repository, "get_by_id")

    test_service = CustomerService(test_repository)
    mocker.patch.object(test_service, "_validate_customer_exists")

    test_service.get_customer(1)
    mock_get_by_id.assert_called_once_with(1)


def test_get_customer_returns_value(mocker: MockerFixture):
    test_repository = CustomerRepository()
    mock_get_by_id = mocker.patch.object(test_repository, "get_by_id")
    mock_get_by_id.return_value = "Test Value"

    test_service = CustomerService(test_repository)
    mocker.patch.object(test_service, "_validate_customer_exists")

    assert test_service.get_customer(1) == "Test Value"


def test_get_customer_by_id_call_get_by_id(mocker: MockerFixture):
    test_repository = CustomerRepository()
    mock_get_by_id = mocker.patch.object(test_repository, "get_by_id")

    test_service = CustomerService(test_repository)

    test_service.get_customer_by_id(1)
    mock_get_by_id.assert_called_once_with(1)


def test_get_customer_by_id_returns_value(mocker: MockerFixture):
    test_repository = CustomerRepository()
    mock_get_by_id = mocker.patch.object(test_repository, "get_by_id")
    mock_get_by_id.return_value = "Test Value"

    test_service = CustomerService(test_repository)

    assert test_service.get_customer_by_id(1) == "Test Value"


def test_get_customer_name_gets_name(mocker: MockerFixture):
    test_repository = CustomerRepository()
    test_service = CustomerService(test_repository)
    mock_get_customer = mocker.patch.object(test_service, "get_customer")
    mock_get_customer.return_value = customer_1

    assert test_service.get_customer_name(1) == customer_1.name


def test_update_customer_calls_update(mocker: MockerFixture):
    test_repository = CustomerRepository()
    mock_update = mocker.patch.object(test_repository, "update")
    mock_update.return_value = "Test Value"

    test_service = CustomerService(test_repository)
    mocker.patch.object(test_service, "_validate_customer_exists")
    mocker.patch.object(test_service, "_validate_customer")
    mocker.patch.object(test_service, "_validate_email_unique")

    test_service.update_customer(1, customer_1)

    mock_update.assert_called_once_with(1, customer_1)


def test_update_customer_returns_value(mocker: MockerFixture):
    test_repository = CustomerRepository()
    mock_update = mocker.patch.object(test_repository, "update")
    mock_update.return_value = customer_1

    test_service = CustomerService(test_repository)
    mocker.patch.object(test_service, "_validate_customer_exists")
    mocker.patch.object(test_service, "_validate_customer")
    mocker.patch.object(test_service, "_validate_email_unique")

    assert test_service.update_customer(1, customer_1) == customer_1


def test_remove_customer_calls_delete(mocker: MockerFixture):
    test_repository = CustomerRepository()
    mock_delete = mocker.patch.object(test_repository, "delete")

    test_service = CustomerService(test_repository)
    mocker.patch.object(test_service, "_validate_customer_exists")

    test_service.remove_customer(1)

    mock_delete.assert_called_once_with(1)


def test_record_purchase_adds_to_lifetime_spent(mocker: MockerFixture):
    previous_spent = customer_1.lifetime_spent

    test_repository = CustomerRepository()
    mock_get_by_id = mocker.patch.object(test_repository, "get_by_id")
    mock_get_by_id.return_value = customer_1
    mock_update = mocker.patch.object(test_repository, "update")
    mock_update.return_value = customer_1

    test_service = CustomerService(test_repository)

    new_customer = test_service.record_purchase(1, Decimal("100.00"))

    assert new_customer.lifetime_spent == previous_spent + Decimal("100.00")


def test_record_purchase_errors_on_no_customer(mocker: MockerFixture):
    test_repository = CustomerRepository()
    mock_get_by_id = mocker.patch.object(test_repository, "get_by_id")
    mock_get_by_id.return_value = None

    test_service = CustomerService(test_repository)

    with raises(CustomerNotFoundError):
        test_service.record_purchase(1, Decimal("100.00"))


def test_record_purchase_returns_customer(mocker: MockerFixture):
    test_repository = CustomerRepository()
    mock_get_by_id = mocker.patch.object(test_repository, "get_by_id")
    mock_get_by_id.return_value = customer_1
    mock_update = mocker.patch.object(test_repository, "update")
    mock_update.return_value = customer_1

    test_service = CustomerService(test_repository)

    assert test_service.record_purchase(1, Decimal("100.00")) == customer_1


def test_validate_customer_passes(mocker: MockerFixture):
    test_repository = CustomerRepository()

    mocker.patch("src.validators.validate_name_not_empty")
    mocker.patch("src.validators.validate_email")
    mocker.patch("src.validators.validate_money_decimal_positive_two_decimal_places")

    test_service = CustomerService(test_repository)

    test_service._validate_customer(customer_1)


def test_validate_customer_exists_calls_get_by_id(mocker: MockerFixture):
    test_repository = CustomerRepository()
    mock_get_by_id = mocker.patch.object(test_repository, "get_by_id")
    test_service = CustomerService(test_repository)

    test_service._validate_customer_exists(1)

    mock_get_by_id.assert_called_once_with(1)


def test_validate_customer_exists_errors_on_not_found(mocker: MockerFixture):
    test_repository = CustomerRepository()
    mock_get_by_id = mocker.patch.object(test_repository, "get_by_id")
    mock_get_by_id.return_value = None

    test_service = CustomerService(test_repository)

    with raises(CustomerNotFoundError):
        test_service._validate_customer_exists(1)


def test_validate_customer_exists_passes_when_found(mocker: MockerFixture):
    test_repository = CustomerRepository()
    mock_get_by_id = mocker.patch.object(test_repository, "get_by_id")
    mock_get_by_id.return_value = customer_1

    test_service = CustomerService(test_repository)

    test_service._validate_customer_exists(1)


def test_validate_email_unique_passes_is_unique(mocker: MockerFixture):
    test_repository = CustomerRepository()
    mock_get_all = mocker.patch.object(test_repository, "get_all")
    mock_get_all.return_value = [customer_1, customer_2]

    test_service = CustomerService(test_repository)
    test_service._validate_email_unique("test.missing@example.com", 1)


def test_validate_email_unique_errors_not_unique(mocker: MockerFixture):
    test_repository = CustomerRepository()
    mock_get_all = mocker.patch.object(test_repository, "get_all")
    mock_get_all.return_value = [customer_1, customer_2]

    test_service = CustomerService(test_repository)

    with raises(CustomerDuplicateEmailError):
        test_service._validate_email_unique(customer_2.email, 1)
