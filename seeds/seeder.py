from flask_seeder import Seeder, Faker, generator
from datetime import datetime
from random import choice, uniform

from app.repositories.models import Beverage, Ingredient, Order, OrderDetail, Size
from seeds.custom_generators import DateTime

SIZES = (
    {'name': 'Small', 'price': 5},
    {'name': 'Medium', 'price': 7},
    {'name': 'Large', 'price': 9},
    {'name': 'Extra Large', 'price': 11},
    {'name': 'Maracanã', 'price': 13},
)

INGREDIENTS = (
    {'name': 'Cheese', 'price': 1},
    {'name': 'Pepperoni', 'price': 1},
    {'name': 'Ham', 'price': 1},
    {'name': 'Bacon', 'price': 1.5},
    {'name': 'Mushrooms', 'price': 1.5},
    {'name': 'Onions', 'price': 1},
    {'name': 'Tomatoes', 'price': 1},
    {'name': 'Olives', 'price': 0.5},
    {'name': 'Pineapple', 'price': 5},
    {'name': 'Anchovies', 'price': 1},
)

BEVERAGES = (
    {'name': 'Coca-Cola', 'price': 2},
    {'name': 'Fanta', 'price': 2},
    {'name': 'Sprite', 'price': 2},
    {'name': 'Water', 'price': 1},
    {'name': 'Beer', 'price': 3},
)

NUMBER_OF_ORDERS = 100
NUMBER_OF_CLIENTS = 8
AVERAGE_DETAILS_PER_ORDER = 5


class DatabaseSeeder(Seeder):

    def create_items(self, model, data: tuple):
        faker = Faker(
            cls=model,
            init={
                '_id': generator.Sequence(end=len(data)),
                'name': '',
                'price': 0,
            }
        )

        created_items = faker.create(len(data))
        for item in created_items:
            item.name = data[item._id - 1]['name']
            item.price = data[item._id - 1]['price']

        return created_items

    def create_orders(self):
        faker = Faker(
            cls=Order,
            init={
                '_id': generator.Sequence(end=NUMBER_OF_ORDERS),
                'client_name': generator.Name(),
                'client_dni': generator.String(pattern='\d{11}'),
                'client_address': generator.String(pattern='\c{8,20}, [1-9]{1}\d{0,3}'),
                'client_phone': generator.String(pattern='\d{10}'),
                'date': DateTime(start=datetime(2022, 1, 1)),
                'total_price': 0,
                'size_id': generator.Integer(end=len(SIZES)),
            }
        )

        created_orders = faker.create(NUMBER_OF_ORDERS)
        clients = created_orders[:NUMBER_OF_CLIENTS]
        for index, order in enumerate(created_orders):
            order.total_price = SIZES[order.size_id - 1]['price']
            if index < NUMBER_OF_CLIENTS:
                continue
            client = choice(clients)
            order.client_name = client.client_name
            order.client_dni = client.client_dni
            order.client_address = client.client_address
            order.client_phone = client.client_phone

        return created_orders

    def create_order_details(self, created_orders, ing_to_bev_factor: float = 0.8):
        number_of_order_details = NUMBER_OF_ORDERS * AVERAGE_DETAILS_PER_ORDER
        faker = Faker(
            cls=OrderDetail,
            init={
                '_id': generator.Sequence(end=number_of_order_details),
                'order_id': generator.Integer(end=NUMBER_OF_ORDERS),
                'price': 0,
            }
        )

        created_order_details = faker.create(number_of_order_details)
        for order_detail in created_order_details:
            if uniform(0, 1) < ing_to_bev_factor:
                order_detail.ingredient_id = choice(range(1, len(INGREDIENTS) + 1))
                order_detail.price = INGREDIENTS[order_detail.ingredient_id - 1]['price']
            else:
                order_detail.beverage_id = choice(range(1, len(BEVERAGES) + 1))
                order_detail.price = BEVERAGES[order_detail.beverage_id - 1]['price']
            created_orders[order_detail.order_id - 1].total_price += order_detail.price

        return created_order_details

    def run(self):
        created_sizes = self.create_items(Size, SIZES)
        created_ingredients = self.create_items(Ingredient, INGREDIENTS)
        created_beverages = self.create_items(Beverage, BEVERAGES)
        created_orders = self.create_orders()
        created_order_details = self.create_order_details(created_orders)

        print('Seeding Sizes...')
        self.db.session.add_all(created_sizes)
        print('Seeding Ingredients...')
        self.db.session.add_all(created_ingredients)
        print('Seeding Beverages...')
        self.db.session.add_all(created_beverages)
        print('Seeding Orders...')
        self.db.session.add_all(created_orders)
        print('Seeding Order Details...')
        self.db.session.add_all(created_order_details)
        self.db.session.commit()
