import pytest
from unittest.mock import Mock

from burger import Burger
from ingredient import Ingredient


class TestBurger:

    # --- set_buns ---

    def test_set_buns_assigns_bun(self):
        bun = Mock()
        bun.get_name.return_value = "black bun"
        bun.get_price.return_value = 100
        burger = Burger()
        burger.set_buns(bun)
        assert burger.bun is bun

    # --- add_ingredient ---

    def test_add_ingredient_appends_to_list(self):
        burger = Burger()
        ingredient = Mock(spec=Ingredient)
        burger.add_ingredient(ingredient)
        assert burger.ingredients == [ingredient]

    def test_add_ingredient_increases_count(self):
        burger = Burger()
        ingredient = Mock(spec=Ingredient)
        burger.add_ingredient(ingredient)
        assert len(burger.ingredients) == 1

    # --- remove_ingredient ---

    def test_remove_ingredient_removes_by_index(self):
        burger = Burger()
        ingredient1 = Mock(spec=Ingredient)
        ingredient2 = Mock(spec=Ingredient)
        burger.add_ingredient(ingredient1)
        burger.add_ingredient(ingredient2)
        burger.remove_ingredient(0)
        assert burger.ingredients == [ingredient2]

    # --- move_ingredient ---

    def test_move_ingredient_changes_position(self):
        burger = Burger()
        ingredient1 = Mock(spec=Ingredient)
        ingredient2 = Mock(spec=Ingredient)
        ingredient3 = Mock(spec=Ingredient)
        burger.add_ingredient(ingredient1)
        burger.add_ingredient(ingredient2)
        burger.add_ingredient(ingredient3)
        burger.move_ingredient(0, 2)
        assert burger.ingredients == [ingredient2, ingredient3, ingredient1]

    # --- get_price ---

    def test_get_price_returns_double_bun_price_without_ingredients(self):
        bun = Mock()
        bun.get_price.return_value = 100
        burger = Burger()
        burger.set_buns(bun)
        assert burger.get_price() == 200

    def test_get_price_includes_ingredient_price(self):
        bun = Mock()
        bun.get_price.return_value = 100
        ingredient = Mock(spec=Ingredient)
        ingredient.get_price.return_value = 50
        burger = Burger()
        burger.set_buns(bun)
        burger.add_ingredient(ingredient)
        assert burger.get_price() == 250

    @pytest.mark.parametrize("bun_price,ingredient_prices,expected", [
        (100, [], 200),
        (100, [50], 250),
        (200, [100, 200], 700),
        (0, [0], 0),
        (100, [50, 50, 50], 350),
    ])
    def test_get_price_parametrized(self, bun_price, ingredient_prices, expected):
        bun = Mock()
        bun.get_price.return_value = bun_price
        burger = Burger()
        burger.set_buns(bun)
        for price in ingredient_prices:
            ingredient = Mock(spec=Ingredient)
            ingredient.get_price.return_value = price
            burger.add_ingredient(ingredient)
        assert burger.get_price() == expected

    # --- get_receipt ---

    def test_get_receipt_starts_with_bun_name(self):
        bun = Mock()
        bun.get_name.return_value = "black bun"
        bun.get_price.return_value = 100
        burger = Burger()
        burger.set_buns(bun)
        receipt = burger.get_receipt()
        assert receipt.startswith("(==== black bun ====)")

    def test_get_receipt_ends_with_price(self):
        bun = Mock()
        bun.get_name.return_value = "black bun"
        bun.get_price.return_value = 100
        burger = Burger()
        burger.set_buns(bun)
        receipt = burger.get_receipt()
        assert receipt.endswith("Price: 200")

    def test_get_receipt_contains_ingredient_line(self):
        bun = Mock()
        bun.get_name.return_value = "black bun"
        bun.get_price.return_value = 100
        ingredient = Mock(spec=Ingredient)
        ingredient.get_type.return_value = "SAUCE"
        ingredient.get_name.return_value = "hot sauce"
        ingredient.get_price.return_value = 50
        burger = Burger()
        burger.set_buns(bun)
        burger.add_ingredient(ingredient)
        receipt = burger.get_receipt()
        assert "= sauce hot sauce =" in receipt

    @pytest.mark.parametrize("ingredient_type,ingredient_name,expected_line", [
        ("SAUCE", "hot sauce", "= sauce hot sauce ="),
        ("FILLING", "cutlet", "= filling cutlet ="),
    ])
    def test_get_receipt_ingredient_line_format(self, ingredient_type, ingredient_name, expected_line):
        bun = Mock()
        bun.get_name.return_value = "black bun"
        bun.get_price.return_value = 100
        ingredient = Mock(spec=Ingredient)
        ingredient.get_type.return_value = ingredient_type
        ingredient.get_name.return_value = ingredient_name
        ingredient.get_price.return_value = 50
        burger = Burger()
        burger.set_buns(bun)
        burger.add_ingredient(ingredient)
        receipt = burger.get_receipt()
        assert expected_line in receipt
