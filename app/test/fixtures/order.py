import pytest
from datetime import datetime

from ..utils.functions import (shuffle_list, get_random_sequence, get_random_sample,
                               get_random_string, get_random_phone, get_random_choice,
                               get_random_date)


def client_data_mock() -> dict:
    return {
        'client_address': get_random_string(),
        'client_dni': get_random_sequence(),
        'client_name': get_random_string(),
        'client_phone': get_random_phone()
    }


@pytest.fixture
def order_uri():
    return '/order/'


@pytest.fixture
def client_data():
    return client_data_mock()


@pytest.fixture
def clients_data():
    return [client_data_mock() for _ in range(3)]


@pytest.fixture
def order(create_beverages, create_ingredients, create_size, client_data) -> dict:
    ingredients = [ingredient.get('_id') for ingredient in create_ingredients]
    beverages = [beverage.get('_id') for beverage in create_beverages]
    size_id = create_size.json['_id']
    return {
        **client_data,
        'ingredients': ingredients,
        'beverages': beverages,
        'size_id': size_id
    }


@pytest.fixture
def orders(create_beverages, create_ingredients, create_size, clients_data) -> list:
    ingredients = [ingredient.get('_id') for ingredient in create_ingredients]
    beverages = [beverage.get('_id') for beverage in create_beverages]
    size_id = create_size.json['_id']
    orders = []
    for _ in range(50):
        client_data = get_random_choice(clients_data)
        orders.append({
            **client_data,
            'ingredients': get_random_sample(ingredients, 3),
            'beverages': get_random_sample(beverages, 2),
            'size_id': size_id,
            'date': get_random_date(start=datetime(2020, 1, 1), end=datetime(2020, 5, 31))
        })
    return orders


@pytest.fixture
def create_order(client, order_uri, create_beverages, create_ingredients, create_size, client_data) -> list:
    ingredients = [ingredient.get('_id') for ingredient in create_ingredients]
    beverages = [beverage.get('_id') for beverage in create_beverages]
    size_id = create_size.json['_id']
    response = client.post(order_uri, json={
        **client_data,
        'ingredients': shuffle_list(ingredients)[:5],
        'beverages': shuffle_list(beverages)[:5],
        'size_id': size_id
    })
    return response


@pytest.fixture
def create_orders(client, order_uri, create_beverages, create_ingredients, create_sizes, client_data) -> list:
    ingredients = [ingredient.get('_id') for ingredient in create_ingredients]
    beverages = [beverage.get('_id') for beverage in create_beverages]
    sizes = [size.get('_id') for size in create_sizes]
    orders = []
    for _ in range(10):
        new_order = client.post(order_uri, json={
            **client_data,
            'ingredients': shuffle_list(ingredients)[:5],
            'beverages': shuffle_list(beverages)[:5],
            'size_id': get_random_choice(sizes)
        })
        orders.append(new_order.json)
    return orders
