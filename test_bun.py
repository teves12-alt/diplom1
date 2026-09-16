import pytest

from bun import Bun


class TestBun:

    def test_init_name_saved(self):
        bun = Bun("black bun", 100)
        assert bun.name == "black bun"

    def test_init_price_saved(self):
        bun = Bun("black bun", 100)
        assert bun.price == 100

    def test_get_name_returns_name(self):
        bun = Bun("black bun", 100)
        assert bun.get_name() == "black bun"

    def test_get_price_returns_price(self):
        bun = Bun("black bun", 100)
        assert bun.get_price() == 100

    @pytest.mark.parametrize("name,price", [
        ("black bun", 100),
        ("white bun", 200),
        ("red bun", 300),
        ("", 0),
    ])
    def test_get_name_parametrized(self, name, price):
        bun = Bun(name, price)
        assert bun.get_name() == name

    @pytest.mark.parametrize("name,price", [
        ("black bun", 100),
        ("white bun", 200),
        ("red bun", 300),
        ("", 0),
    ])
    def test_get_price_parametrized(self, name, price):
        bun = Bun(name, price)
        assert bun.get_price() == price
