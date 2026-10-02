"""Application entry point."""

from src.repositories.customer_repository import CustomerRepository
from src.services.customer_service import CustomerService

customer_repository = CustomerRepository()
customer_service = CustomerService(customer_repository)
