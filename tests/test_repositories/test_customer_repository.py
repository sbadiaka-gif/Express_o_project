# pyright: reportPrivateUsage = false

from decimal import Decimal

from src.models.customer import Customer
from src.repositories.customer_repository import CustomerRepository

customer_1 = Customer(
    "Alice Johnson",
    "alice.johnson@example.com",
    Decimal("245.50"),
)

customer_2 = Customer(
    "Brian Smith",
    "brian.smith@example.com",
    Decimal("00.00"),
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


def test_add_returns_object():
    test_repository = CustomerRepository()
    assert test_repository.add(customer_1) == customer_1


def test_add_saves_object():
    test_repository = CustomerRepository()
    test_repository.add(customer_1)
    assert test_repository._customers[0] == customer_1


def test_get_by_id_gets():
    test_repository = CustomerRepository()
    customer_1.id = 1
    test_repository._customers.append(customer_1)
    assert test_repository.get_by_id(1)


def test_get_by_id_gets_none_when_no_items():
    test_repository = CustomerRepository()
    assert not test_repository.get_by_id(1)


def test_get_by_id_gets_none_when_id_missing():
    test_repository = CustomerRepository()
    customer_1.id = 1
    test_repository._customers.append(customer_1)
    assert not test_repository.get_by_id(0)


def test_get_all_gets_none_when_no_items():
    test_repository = CustomerRepository()
    assert test_repository.get_all() == []


def test_get_all_gets_all():
    test_repository = CustomerRepository()
    test_repository._customers.append(customer_1)
    test_repository._customers.append(customer_2)
    assert test_repository.get_all()


def test_update_returns_item():
    test_repository = CustomerRepository()
    customer_1.id = 1
    test_repository._customers.append(customer_1)
    customer_2.id = 2
    test_repository._customers.append(customer_2)
    assert test_repository.update(2, customer_3) == customer_3


def test_update_returns_none_missing_id():
    test_repository = CustomerRepository()
    assert not test_repository.update(1, customer_1)


def test_update_updates_item():
    test_repository = CustomerRepository()
    customer_1.id = 1
    test_repository._customers.append(customer_1)
    customer_2.id = 2
    test_repository._customers.append(customer_2)
    test_repository.update(2, customer_3)
    assert test_repository._customers[1] == customer_3


def test_delete_returns_true_on_remove():
    test_repository = CustomerRepository()
    customer_1.id = 1
    test_repository._customers.append(customer_1)
    customer_2.id = 2
    test_repository._customers.append(customer_2)
    assert test_repository.delete(1)


def test_delete_returns_false_on_not_remove():
    test_repository = CustomerRepository()
    assert not test_repository.delete(1)


def test_delete_removes_item():
    test_repository = CustomerRepository()
    customer_1.id = 1
    test_repository._customers.append(customer_1)
    customer_2.id = 2
    test_repository._customers.append(customer_2)
    test_repository.delete(2)
    assert len(test_repository._customers) == 1
