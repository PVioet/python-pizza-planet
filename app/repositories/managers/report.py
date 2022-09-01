from sqlalchemy import func, desc

from .base import BaseManager
from ..models import Beverage, Ingredient, OrderDetail, Order


class ReportManager(BaseManager):

    @classmethod
    def get_most_requested_ingredient(cls):
        most_requested_ingredient, quantity = cls.session.query(
            Ingredient, func.count(OrderDetail.ingredient_id).label('quantity')).join(OrderDetail).group_by(
            Ingredient._id).order_by(
            desc('quantity')).first()
        return [most_requested_ingredient.name, quantity] or [None, 0]

    @classmethod
    def get_most_requested_beverage(cls):
        most_requested_beverage, quantity = cls.session.query(
            Beverage, func.count(OrderDetail.beverage_id).label('quantity')).join(OrderDetail).group_by(
            Beverage._id).order_by(
            desc('quantity')).first()
        return [most_requested_beverage.name, quantity] or [None, 0]

    @classmethod
    def get_month_with_more_revenue(cls):
        date, amount = cls.session.query(func.strftime('%Y-%m', Order.date).label('month'), func.sum(Order.total_price).label('amount')).group_by('month').order_by(desc('amount')).first()
        return [date, amount] or [None, 0]

    @classmethod
    def get_best_customers(cls, limit: int = 3):
        best_customers = cls.session.query(Order.client_name, func.sum(Order.total_price)).group_by(
            Order.client_name).order_by(func.sum(Order.total_price).desc()).limit(limit).all()
        best_customers = list(map(list, best_customers))
        return best_customers or []
