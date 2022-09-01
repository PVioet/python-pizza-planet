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

    most_requested_ingredient_count = max(ingredient_count.values())
    most_requested_ingredient_ids = [ingredient_id for ingredient_id, count in ingredient_count.items() if count == most_requested_ingredient_count]
    most_requested_ingredients = []
    for ingredient_id in most_requested_ingredient_ids:
        ingredient, _ = IngredientController.get_by_id(ingredient_id)
        most_requested_ingredients.append(ingredient['name'])
        
    most_requested_beverage_count = max(beverage_count.values())
    most_requested_beverage_ids = [beverage_id for beverage_id, count in beverage_count.items() if count == most_requested_beverage_count]
    most_requested_beverages = []
    for beverage_id in most_requested_beverage_ids:
        beverage, _ = BeverageController.get_by_id(beverage_id)
        most_requested_beverages.append(beverage['name'])
    
    month_with_more_revenue = max(month_count, key=month_count.get)
    best_customers = sorted(client_count.items(), key=lambda x: x[1], reverse=True)[:3]
    best_customers = list(map(list, best_customers))

    created_report, error = ReportController.generate()
    pytest.assume(error is None)
    pytest.assume(created_report['ingredient'] in most_requested_ingredients)
    pytest.assume(created_report['beverage'] in most_requested_beverages)
    pytest.assume(created_report['month'] == month_with_more_revenue)
    pytest.assume(created_report['customers'] == best_customers)
