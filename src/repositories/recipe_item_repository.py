from src.models.recipe_item import RecipeItem

class RecipeItemRepository:
    def __init__(self):
        self._recipe_items: list[RecipeItem] = []
        self._next_id: int = 1

    def add_recipe_item(self, recipe_item: RecipeItem) -> RecipeItem:
        recipe_item.id = self._next_id
        self._next_id += 1
        self._recipe_items.append(recipe_item)
        return recipe_item

    def get_recipe_item_by_id(self, recipe_item_id: int) -> RecipeItem | None:
        for recipe_item in self._recipe_items:
            if recipe_item.id == recipe_item_id:
                return recipe_item
        return None

    def get_all_recipe_items(self) -> list[RecipeItem]:
        return list(self._recipe_items)

    def update_recipe_item(self, updated_recipe_item: RecipeItem) -> RecipeItem | None:
        for index, recipe_item in enumerate(self._recipe_items):
            if recipe_item.id == updated_recipe_item.id:
                self._recipe_items[index] = updated_recipe_item
                return updated_recipe_item
        return None

    def delete_recipe_item(self, recipe_item_id: int) -> bool:
        for index, recipe_item in enumerate(self._recipe_items):
            if recipe_item.id == recipe_item_id:
                del self._recipe_items[index]
                return True
        return False