from typing import List

from .base import BaseManager
from ..models import Order, Ingredient, Beverage, OrderDetail
from ..serializers import OrderSerializer


class OrderManager(BaseManager):
    model = Order
    serializer = OrderSerializer

    @classmethod
    def create(cls, order_data: dict, ingredients: List[Ingredient], beverages: List[Beverage]):
        new_order = cls.model(**order_data)
        cls.session.add(new_order)
        cls.session.flush()
        cls.session.refresh(new_order)
        cls.session.add_all((OrderDetail(order_id=new_order._id, ingredient_id=ingredient._id, price=ingredient.price)
                             for ingredient in ingredients))
        cls.session.add_all((OrderDetail(order_id=new_order._id, beverage_id=beverage._id, price=beverage.price)
                             for beverage in beverages))
        cls.session.commit()
        return cls.serializer().dump(new_order)

    @classmethod
    def update(cls):
        raise NotImplementedError(f'Method not suported for {cls.__name__}')
