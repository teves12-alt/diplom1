import pytest
from unittest.mock import Mock

from praktikum.bun import Bun
from praktikum.ingredient import Ingredient
from praktikum.burger import Burger


# ── Константы формата чека ──────────────────────────────────────
# Вынесены в модульные константы: если формат изменится,
# достаточно поправить одно место — все тесты подхватят.

BUN_LINE = "(==== {} ====)"
INGREDIENT_LINE = "= {} {} ="
PRICE_LINE = "Price: {}"


# ── Фикстуры ────────────────────────────────────────────────────

@pytest.fixture
def burger():
    """Чистый бургер без булочки и ингредиентов."""
    return Burger()


@pytest.fixture
def mock_bun():
    """Мок булочки с предустановленными именем и ценой."""
    bun = Mock(spec=Bun)
    bun.get_name.return_value = "test bun"
    bun.get_price.return_value = 100.0
    return bun


@pytest.fixture
def burger_with_bun(burger, mock_bun):
    """Бургер с установленной булочкой."""
    burger.set_buns(mock_bun)
    return burger


def make_mock_ingredient(ing_type="SAUCE", ing_name="hot sauce", ing_price=50.0):
    """Хелпер для создания мока ингредиента.
    Не фикстура — каждый ингредиент должен быть уникальным объектом."""
    mock_ing = Mock(spec=Ingredient)
    mock_ing.get_type.return_value = ing_type
    mock_ing.get_name.return_value = ing_name
    mock_ing.get_price.return_value = ing_price
    return mock_ing


# ── Тесты: __init__ ─────────────────────────────────────────────

class TestBurgerInit:

    def test_bun_is_none(self, burger):
        assert burger.bun is None

    def test_ingredients_is_empty_list(self, burger):
        assert burger.ingredients == []
        assert isinstance(burger.ingredients, list)


# ── Тесты: set_buns ─────────────────────────────────────────────

class TestBurgerSetBuns:

    def test_assigns_bun(self, burger, mock_bun):
        burger.set_buns(mock_bun)
        assert burger.bun is mock_bun


# ── Тесты: add_ingredient ───────────────────────────────────────

class TestBurgerAddIngredient:

    @pytest.mark.parametrize("count", [1, 2, 3, 5])
    def test_appends_to_list(self, burger, count):
        for _ in range(count):
            burger.add_ingredient(make_mock_ingredient())
        assert len(burger.ingredients) == count

    def test_preserves_order(self, burger):
        first = make_mock_ingredient(ing_name="first")
        second = make_mock_ingredient(ing_name="second")
        burger.add_ingredient(first)
        burger.add_ingredient(second)
        assert burger.ingredients[0] is first
        assert burger.ingredients[1] is second


# ── Тесты: remove_ingredient ────────────────────────────────────

class TestBurgerRemoveIngredient:

    def test_removes_by_index(self, burger):
        ing1 = make_mock_ingredient(ing_name="ing1")
        ing2 = make_mock_ingredient(ing_name="ing2")
        ing3 = make_mock_ingredient(ing_name="ing3")
        burger.add_ingredient(ing1)
        burger.add_ingredient(ing2)
        burger.add_ingredient(ing3)

        burger.remove_ingredient(1)

        assert len(burger.ingredients) == 2
        assert ing2 not in burger.ingredients
        assert burger.ingredients[0] is ing1
        assert burger.ingredients[1] is ing3

    @pytest.mark.parametrize("index", [0, 1])
    def test_removes_from_two(self, burger, index):
        ing1 = make_mock_ingredient(ing_name="ing1")
        ing2 = make_mock_ingredient(ing_name="ing2")
        burger.add_ingredient(ing1)
        burger.add_ingredient(ing2)

        burger.remove_ingredient(index)

        assert len(burger.ingredients) == 1

    # ── Негативные сценарии ──

    def test_raises_index_error_on_out_of_range(self, burger):
        """Удаление по несуществующему индексу выбрасывает IndexError.
        Реализация: del self.ingredients[index] — выбрасывает IndexError."""
        burger.add_ingredient(make_mock_ingredient())

        with pytest.raises(IndexError):
            burger.remove_ingredient(5)

    def test_raises_index_error_on_empty_list(self, burger):
        """Удаление из пустого списка выбрасывает IndexError."""
        with pytest.raises(IndexError):
            burger.remove_ingredient(0)


# ── Тесты: move_ingredient ──────────────────────────────────────

class TestBurgerMoveIngredient:

    @pytest.mark.parametrize("old_index, new_index, expected", [
        (0, 1, [1, 0]),
        (1, 0, [1, 0]),
        (0, 2, [1, 2, 0]),
        (2, 0, [2, 0, 1]),
    ])
    def test_changes_order(self, burger, old_index, new_index, expected):
        for i in range(3):
            mock_ing = Mock(spec=Ingredient)
            mock_ing.id = i
            burger.add_ingredient(mock_ing)

        burger.move_ingredient(old_index, new_index)

        actual_ids = [ing.id for ing in burger.ingredients]
        assert actual_ids == expected

    # ── Негативные сценарии ──

    def test_raises_index_error_on_invalid_old_index(self, burger):
        """move_ingredient с несуществующим old_index выбрасывает IndexError.
        Реализация: self.ingredients.pop(index) — выбрасывает IndexError."""
        for _ in range(3):
            burger.add_ingredient(make_mock_ingredient())

        with pytest.raises(IndexError):
            burger.move_ingredient(10, 0)

    def test_invalid_new_index_moves_to_end(self, burger):
        """move_ingredient с new_index за пределами списка не выбрасывает
        ошибку — list.insert() вставляет элемент в конец.
        Реализация: self.ingredients.insert(new_index, ...) — если
        new_index >= len, элемент добавляется в конец списка."""
        for i in range(3):
            mock_ing = Mock(spec=Ingredient)
            mock_ing.id = i
            burger.add_ingredient(mock_ing)

        burger.move_ingredient(0, 10)

        assert len(burger.ingredients) == 3
        # Элемент 0 переместился в конец
        assert burger.ingredients[-1].id == 0
        assert burger.ingredients[0].id == 1
        assert burger.ingredients[1].id == 2


# ── Тесты: get_price ────────────────────────────────────────────

class TestBurgerGetPrice:

    @pytest.mark.parametrize("bun_price, ing_prices, expected", [
        (100.0, [], 200.0),
        (100.0, [50.0], 250.0),
        (100.0, [50.0, 30.0], 280.0),
        (100.0, [50.0, 30.0, 20.0], 300.0),
        (0.0, [], 0.0),
        (50.0, [0.0, 0.0], 100.0),
        (99.99, [10.01, 20.0], 230.0),
    ])
    def test_calculates_price(self, burger, bun_price, ing_prices, expected):
        mock_b = Mock(spec=Bun)
        mock_b.get_price.return_value = bun_price
        burger.set_buns(mock_b)

        for price in ing_prices:
            mock_ing = Mock(spec=Ingredient)
            mock_ing.get_price.return_value = price
            burger.add_ingredient(mock_ing)

        assert burger.get_price() == expected

    def test_calls_bun_get_price_once_and_multiplies(self, burger_with_bun, mock_bun):
        """get_price() вызывает bun.get_price() ровно 1 раз
        и умножает на 2 (верхняя + нижняя булочка)."""
        result = burger_with_bun.get_price()

        mock_bun.get_price.assert_called_once()
        assert result == 200.0

    def test_calls_each_ingredient_get_price_once(self, burger_with_bun):
        """get_price() вызывает get_price() у каждого ингредиента 1 раз."""
        mock_ings = []
        for _ in range(3):
            mi = make_mock_ingredient(ing_price=50.0)
            mock_ings.append(mi)
            burger_with_bun.add_ingredient(mi)

        burger_with_bun.get_price()

        for mi in mock_ings:
            mi.get_price.assert_called_once()

    # ── Негативные сценарии ──

    @pytest.mark.parametrize("bun_price, expected", [
        (-100.0, -200.0),
        (-50.0, -100.0),
    ])
    def test_handles_negative_bun_price(self, burger, bun_price, expected):
        """Отрицательная цена булочки: get_price() не валидирует знак —
        возвращает математически корректный результат.
        Тесты фиксируют это поведение (см. README — «Отрицательные цены»)."""
        mock_b = Mock(spec=Bun)
        mock_b.get_price.return_value = bun_price
        burger.set_buns(mock_b)

        assert burger.get_price() == expected

    @pytest.mark.parametrize("ing_price, expected", [
        (-50.0, 150.0),    # 200 (булочка) + (-50) = 150
        (-200.0, 0.0),     # 200 + (-200) = 0
    ])
    def test_handles_negative_ingredient_price(self, burger_with_bun, ing_price, expected):
        """Отрицательная цена ингредиента: сумма вычисляется корректно.
        Валидация знака отсутствует — поведение задокументировано в README."""
        mock_ing = Mock(spec=Ingredient)
        mock_ing.get_price.return_value = ing_price
        burger_with_bun.add_ingredient(mock_ing)

        assert burger_with_bun.get_price() == expected


# ── Тесты: get_receipt ──────────────────────────────────────────

class TestBurgerGetReceipt:

    @pytest.mark.parametrize("bun_name, ingredients, expected_price", [
        ("white bun", [], 200.0),
        ("black bun", [("SAUCE", "hot sauce", 50.0)], 250.0),
        ("black bun", [("SAUCE", "hot sauce", 50.0), ("FILLING", "cutlet", 100.0)], 350.0),
    ])
    def test_structure(self, bun_name, ingredients, expected_price):
        """Проверяем структуру чека без привязки к хрупким индексам:
        1. Первая строка — верхняя булочка
        2. Последняя строка — цена
        3. Перед ценой — пустая строка-разделитель
        4. Перед разделителем — нижняя булочка
        5. Между булочками — строки ингредиентов (тип в нижнем регистре)
        """
        burger = Burger()
        mock_b = Mock(spec=Bun)
        mock_b.get_name.return_value = bun_name
        mock_b.get_price.return_value = 100.0
        burger.set_buns(mock_b)

        for ing_type, ing_name, ing_price in ingredients:
            burger.add_ingredient(make_mock_ingredient(ing_type, ing_name, ing_price))

        receipt = burger.get_receipt()
        lines = receipt.split("\n")

        expected_bun = BUN_LINE.format(bun_name)
        expected_price_line = PRICE_LINE.format(expected_price)

        # Первая строка — верхняя булочка
        assert lines[0] == expected_bun
        # Последняя строка — цена
        assert lines[-1] == expected_price_line
        # Перед ценой — пустая строка-разделитель
        assert lines[-2] == ""
        # Перед разделителем — нижняя булочка
        assert lines[-3] == expected_bun

        # Между верхней и нижней булочкой — строки ингредиентов
        ingredient_lines = lines[1:-3]
        assert len(ingredient_lines) == len(ingredients)
        for i, (ing_type, ing_name, _) in enumerate(ingredients):
            expected_ing = INGREDIENT_LINE.format(ing_type.lower(), ing_name)
            assert ingredient_lines[i] == expected_ing

    def test_no_ingredients(self, burger_with_bun):
        """Чек без ингредиентов: 4 строки — верх, низ, пустая, цена."""
        receipt = burger_with_bun.get_receipt()
        lines = receipt.split("\n")

        assert len(lines) == 4
        assert lines[0] == BUN_LINE.format("test bun")
        assert lines[1] == BUN_LINE.format("test bun")
        assert lines[2] == ""
        assert lines[3] == PRICE_LINE.format(200.0)

    def test_calls_bun_get_name_twice(self, burger_with_bun, mock_bun):
        """get_receipt вызывает bun.get_name() ровно 2 раза:
        верхняя и нижняя булочка."""
        burger_with_bun.get_receipt()
        assert mock_bun.get_name.call_count == 2

    def test_indirectly_uses_bun_price_via_get_price(self, burger_with_bun, mock_bun):
        """get_receipt() не запрашивает цену булочки напрямую —
        он вызывает self.get_price(), который внутри обращается
        к bun.get_price() ровно 1 раз. Проверяем всю цепочку целиком."""
        receipt = burger_with_bun.get_receipt()

        mock_bun.get_price.assert_called_once()
        assert PRICE_LINE.format(200.0) in receipt

    def test_ingredient_methods_called_once_each(self, burger_with_bun):
        """Каждый ингредиент: get_type и get_name — по 1 вызову."""
        mock_ing = make_mock_ingredient("SAUCE", "ketchup", 30.0)
        burger_with_bun.add_ingredient(mock_ing)

        burger_with_bun.get_receipt()

        mock_ing.get_type.assert_called_once()
        mock_ing.get_name.assert_called_once()

    def test_ingredient_type_lowercased(self, burger_with_bun):
        """Тип ингредиента приводится к нижнему регистру."""
        mock_ing = make_mock_ingredient("FILLING", "cheese", 75.0)
        burger_with_bun.add_ingredient(mock_ing)

        receipt = burger_with_bun.get_receipt()

        assert INGREDIENT_LINE.format("filling", "cheese") in receipt
        assert INGREDIENT_LINE.format("FILLING", "cheese") not in receipt
