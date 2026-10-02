"""Application entry point."""

from src.repositories.customer_repository import CustomerRepository
from src.repositories.baked_good_repository import BakedGoodRepository

from src.services.customer_service import CustomerService
from src.services.baked_good_service import BakedGoodService

customer_repository = CustomerRepository()
baked_good_repository = BakedGoodRepository()

customer_service = CustomerService(customer_repository)
baked_good_service = BakedGoodService(baked_good_repository)
