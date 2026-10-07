"""Application entry point."""

from decimal import Decimal

# models import
from src.models.customer import Customer
from src.models.baked_good import BakedGood
from src.models.drink import Drink  
from src.models.ingredient import Ingredient
from src.models.purchase import Purchase
from src.models.recipe_item import RecipeItem

#repository imports
from src.repositories.customer_repository import CustomerRepository
from src.repositories.baked_good_repository import BakedGoodRepository
from src.repositories.drink_repository import DrinkRepository
from src.repositories.ingredient_repository import IngredientRepository
from src.repositories.purchase_repository import PurchaseRepository

# service imports
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

from decimal import Decimal
from src.models.recipe_item import RecipeItem

# --- seed ingredients (through the service, not the repository) ---
milk = ingredient_service.add_ingredient(
    Ingredient(
        name="Milk",
        purchasing_cost=Decimal("1.00"),
        unit_amount=Decimal("20.00"),
        unit_of_measure="kg",
    )
)
espresso = ingredient_service.add_ingredient(
    Ingredient(
        name="Espresso Beans",
        purchasing_cost=Decimal("2.00"),
        unit_amount=Decimal("10.00"),
        unit_of_measure="kg",
    )
)

# --- seed drinks ---
latte = drink_service.add_drink(
    Drink(
        name="Latte",
        recipe=[
            RecipeItem(ingredient_id=espresso.id, quantity=Decimal("1.00")),
            RecipeItem(ingredient_id=milk.id, quantity=Decimal("2.00")),
        ],
        markup_percentage=Decimal("0.50"),
        cost_to_produce=Decimal("4.00"),
        sale_price=Decimal("6.00"),
    )
)
espresso_shot = drink_service.add_drink(
    Drink(
        name="Espresso",
        recipe=[RecipeItem(ingredient_id=espresso.id, quantity=Decimal("1.00"))],
        markup_percentage=Decimal("0.50"),
        cost_to_produce=Decimal("2.00"),
        sale_price=Decimal("3.00"),
    )
)

# --- try a sale ---
# if __name__ == "__main__":
#     purchase = purchase_service.purchase_a_drink("Maria", "maria@example.com", latte.id)
#     print(purchase)
#     print(ingredient_service.get_by_id(milk.id))
#     print(ingredient_service.get_by_id(espresso.id))
#     print(customer_service.get_by_email("maria@example.com"))