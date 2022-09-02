from sqlalchemy import func, desc

from .base import BaseManager
from ..models import Beverage, Ingredient, OrderDetail, Order


class ReportManager(BaseManager):

    @classmethod
    def get_most_requested_ingredient(cls):
        query = cls.session.query(
            Ingredient, func.count(OrderDetail.ingredient_id).label('quantity')).join(OrderDetail).group_by(
            Ingredient._id).order_by(
            desc('quantity')).first()
        if query:
            most_requested_ingredient, quantity = query
            return [most_requested_ingredient.name, quantity]
        return []

    @classmethod
    def get_most_requested_beverage(cls):
        query = cls.session.query(
            Beverage, func.count(OrderDetail.beverage_id).label('quantity')).join(OrderDetail).group_by(
            Beverage._id).order_by(
            desc('quantity')).first()
        if query:
            most_requested_beverage, quantity = query
            return [most_requested_beverage.name, quantity]
        return []

    @classmethod
    def get_month_with_more_revenue(cls):
        query = cls.session.query(func.strftime('%Y-%m', Order.date).label('month'), func.sum(Order.total_price).label('amount')).group_by(
            'month').order_by(desc('amount')).first()
        if query:
            month, amount = query
            return [month, amount]
        return []

    @classmethod
    def get_best_customers(cls, limit: int = 3):
        best_customers = cls.session.query(Order.client_name, func.sum(Order.total_price)).group_by(
            Order.client_name).order_by(func.sum(Order.total_price).desc()).limit(limit).all()
        if best_customers:
            return list(map(list, best_customers))
        return []
