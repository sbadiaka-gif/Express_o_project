"""Customer repository."""
from src.models.customer import Customer
from copy import deepcopy

class CustomerRepository:
    def __init__(self):
        self._Customers: list[Customer] = []
        self._next_id: int = 1

    def add(self, Customer: Customer) -> Customer:
        Customer.id = self._next_id
        self._next_id += 1
        self._Customers.append(Customer)
        return Customer
    
    def get_by_id(self, Customer_id: int) -> Customer | None:
        for Customer in self._Customers:
            if Customer.id == Customer_id:
                return deepcopy(Customer)
        
        return None
    
    def get_all(self) -> list[Customer]:
        return deepcopy(self._Customers)
    
    def update(self, updated_Customer: Customer) -> Customer | None:
        for index, Customer in enumerate(self._Customers):
            if Customer.id == updated_Customer.id:
                self._Customers[index] = updated_Customer
                return deepcopy(updated_Customer)
        
        return None
    
    def delete(self, Customer_id: int) -> bool:
        for index, Customer in enumerate(self._Customers):
            if Customer.id == Customer_id:
                del self._Customers[index]
                return True
        
        return False