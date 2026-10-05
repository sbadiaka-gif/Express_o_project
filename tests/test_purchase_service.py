from datetime import datetime, timezone
from decimal import Decimal

from src.models.customer import Customer
from src.models.drink import Drink
from src.models.purchase import Purchase
from src.models.purchase_item import PurchaseItem
from src.repositories.purchase_repository import PurchaseRepository
from src.services.purchase_service import PurchaseService


class FakeCustomerService:
    def __init__(self):
        self.customer = Customer(name="Alice", email="alice@example.com")
        self.recorded = []

    def get_customer_by_id(self, customer_id):
        return self.customer if customer_id == 1 else None

    def record_purchase(self, customer_id, amount):
        self.recorded.append((customer_id, amount))


class FakeDrinkService:
    def __init__(self):
        self.drink = Drink(
            name="Latte", markup_percentage=Decimal("0.20"), sale_price=Decimal("5.00")
        )

    def get_drink_by_id(self, drink_id):
        return self.drink if drink_id == 7 else None


class FakeBakedGoodService:
    def __init__(self):
        self.item = None

    def get_baked_good_by_id(self, baked_good_id):
        return self.item if baked_good_id == 8 else None


def test_create_purchase_sets_total_and_records_customer_spend():
    customer_service = FakeCustomerService()
    drink_service = FakeDrinkService()
    baked_good_service = FakeBakedGoodService()
    repository = PurchaseRepository()
    service = PurchaseService(
        repository, customer_service, drink_service, baked_good_service
    )

    purchase = Purchase(
        customer_id=1,
        items=[
            PurchaseItem(
                item_type="drink", item_id=7, quantity=2, unit_price=Decimal("0.00")
            ),
        ],
        timestamp=datetime.now(timezone.utc),
    )

    created = service.create_purchase(purchase)

    assert created.total_cost == Decimal("10.00")
    assert created.items[0].unit_price == Decimal("5.00")
    assert customer_service.recorded == [(1, Decimal("10.00"))]
    assert created.id == 1
