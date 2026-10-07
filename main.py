"""Application entry point."""
from src.models.customer import Customer
from src.models.baked_good import BakedGood
from src.models.drink import Drink  
from src.models.ingredient import Ingredient
from src.models.purchase import Purchase

from src.repositories.customer_repository import CustomerRepository
from src.repositories.baked_good_repository import BakedGoodRepository
from src.repositories.drink_repository import DrinkRepository
from src.repositories.ingredient_repository import IngredientRepository
from src.repositories.purchase_repository import PurchaseRepository
from src.services.customer_service import CustomerService
from src.services.baked_good_service import BakedGoodService
from src.services.drink_service import DrinkService
from src.services.ingredient_service import IngredientService
from src.services.purchase_service import PurchaseService

customer_repository = CustomerRepository()
customer_service = CustomerService(customer_repository)
baked_good_repository = BakedGoodRepository()
baked_good_service = BakedGoodService(baked_good_repository)
ingredient_repository = IngredientRepository()
ingredient_service = IngredientService(ingredient_repository)
drink_repository = DrinkRepository()
drink_service = DrinkService(drink_repository, ingredient_service)
purchase_repository = PurchaseRepository()
purchase_service = PurchaseService(
    purchase_repository,
    customer_service,
    drink_service,
    baked_good_service,
    ingredient_service,
)
