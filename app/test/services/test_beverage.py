import pytest


def test_create_beverage_service(create_beverage):
    beverage = create_beverage.json
    pytest.assume(create_beverage.status.startswith('200'))
    pytest.assume(beverage['_id'])
    pytest.assume(beverage['name'])
    pytest.assume(beverage['price'])
