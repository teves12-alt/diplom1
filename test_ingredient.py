import pytest

from ingredient import Ingredient
from ingredient_types import INGREDIENT_TYPE_SAUCE, INGREDIENT_TYPE_FILLING


class TestIngredient:

    def test_init_type_saved(self):
        ingredient = Ingredient(INGREDIENT_TYPE_SAUCE, "hot sauce", 100)
        assert ingredient.type == INGREDIENT_TYPE_SAUCE

    def test_init_name_saved(self):
        ingredient = Ingredient(INGREDIENT_TYPE_SAUCE, "hot sauce", 100)
        assert ingredient.name == "hot sauce"

    def test_init_price_saved(self):
        ingredient = Ingredient(INGREDIENT_TYPE_SAUCE, "hot sauce", 100)
        assert ingredient.price == 100

    def test_get_type_returns_type(self):
        ingredient = Ingredient(INGREDIENT_TYPE_FILLING, "cutlet", 100)
        assert ingredient.get_type() == INGREDIENT_TYPE_FILLING

    def test_get_name_returns_name(self):
        ingredient = Ingredient(INGREDIENT_TYPE_FILLING, "cutlet", 100)
        assert ingredient.get_name() == "cutlet"

    def test_get_price_returns_price(self):
        ingredient = Ingredient(INGREDIENT_TYPE_FILLING, "cutlet", 100)
        assert ingredient.get_price() == 100

    @pytest.mark.parametrize("ingredient_type,name,price", [
        (INGREDIENT_TYPE_SAUCE, "hot sauce", 100),
        (INGREDIENT_TYPE_SAUCE, "sour cream", 200),
        (INGREDIENT_TYPE_FILLING, "cutlet", 100),
        (INGREDIENT_TYPE_FILLING, "sausage", 300),
    ])
    def test_get_type_parametrized(self, ingredient_type, name, price):
        ingredient = Ingredient(ingredient_type, name, price)
        assert ingredient.get_type() == ingredient_type

    @pytest.mark.parametrize("ingredient_type,name,price", [
        (INGREDIENT_TYPE_SAUCE, "hot sauce", 100),
        (INGREDIENT_TYPE_FILLING, "cutlet", 100),
    ])
    def test_get_name_parametrized(self, ingredient_type, name, price):
        ingredient = Ingredient(ingredient_type, name, price)
        assert ingredient.get_name() == name

    @pytest.mark.parametrize("ingredient_type,name,price", [
        (INGREDIENT_TYPE_SAUCE, "hot sauce", 100),
        (INGREDIENT_TYPE_FILLING, "cutlet", 100),
    ])
    def test_get_price_parametrized(self, ingredient_type, name, price):
        ingredient = Ingredient(ingredient_type, name, price)
        assert ingredient.get_price() == price
