from sqlalchemy import func

from .base import BaseManager
from ..models import Beverage, Ingredient, OrderDetail, Order


class ReportManager(BaseManager):

    @classmethod
    def get_most_requested_ingredient(cls):
        most_requested_ingredient = cls.session.query(Ingredient).join(OrderDetail).group_by(
            Ingredient._id).order_by(func.count(OrderDetail.ingredient_id).desc()).first()
        return most_requested_ingredient.name or None

    @classmethod
    def get_most_requested_beverage(cls):
        most_requested_beverage = cls.session.query(Beverage).join(OrderDetail).group_by(
            Beverage._id).order_by(func.count(OrderDetail.beverage_id).desc()).first()
        return most_requested_beverage.name or None

    @classmethod
    def get_month_with_more_revenue(cls):
        date = cls.session.query(func.strftime('%Y-%m', Order.date).label('month')).group_by('month').order_by(func.sum(Order.total_price).desc()).first()
        return date[0] or None

    @classmethod
    def get_best_customers(cls, limit: int = 3):
        best_customers = cls.session.query(Order.client_name, func.sum(Order.total_price)).group_by(
            Order.client_name).order_by(func.sum(Order.total_price).desc()).limit(limit).all()
        best_customers = list(map(list, best_customers))
        return best_customers or []
