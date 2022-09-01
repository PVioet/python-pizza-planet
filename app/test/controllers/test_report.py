import pytest
from collections import defaultdict
from datetime import datetime
from app.controllers import ReportController, OrderController, IngredientController, BeverageController


def test_generate(app, orders: list):
    ingredient_count = defaultdict(int)
    beverage_count = defaultdict(int)
    month_count = defaultdict(float)
    client_count = defaultdict(float)
    for order in orders:
        created_order, _ = OrderController.create(order)
        for ingredient in order.pop('ingredients', []):
            ingredient_count[ingredient] += 1
        for beverage in order.pop('beverages', []):
            beverage_count[beverage] += 1
        date = datetime.strptime(created_order['date'], '%Y-%m-%dT%H:%M:%S.%f').strftime('%Y-%m')
        month_count[date] += created_order['total_price']
        client_count[created_order['client_name']] += created_order['total_price']

    most_requested_ingredient_id = max(ingredient_count, key=ingredient_count.get)
    most_requested_beverage_id = max(beverage_count, key=beverage_count.get)
    month_with_more_revenue = max(month_count, key=month_count.get)
    best_customers = sorted(client_count.items(), key=lambda x: x[1], reverse=True)[:3]

    most_requested_ingredient = IngredientController.get_by_id(most_requested_ingredient_id)[0]['name']
    most_requested_beverage = BeverageController.get_by_id(most_requested_beverage_id)[0]['name']

    created_report, error = ReportController.generate()
    pytest.assume(error is None)
    pytest.assume(created_report['ingredient'] == most_requested_ingredient)
    pytest.assume(created_report['beverage'] == most_requested_beverage)
    pytest.assume(created_report['month'] == month_with_more_revenue)
    pytest.assume(created_report['customers'] == best_customers)
