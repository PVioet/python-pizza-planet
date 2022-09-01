from sqlalchemy.exc import SQLAlchemyError

from .base import BaseController
from ..repositories.managers import ReportManager


class ReportController(BaseController):
    manager = ReportManager

    @classmethod
    def generate(cls):
        try:
            report_data = {}
            report_data['ingredient'] = cls.manager.get_most_requested_ingredient()
            report_data['beverage'] = cls.manager.get_most_requested_beverage()
            report_data['month'] = cls.manager.get_month_with_more_revenue()
            report_data['customers'] = cls.manager.get_best_customers()
            return report_data, None
        except (SQLAlchemyError, RuntimeError) as ex:
            return None, str(ex)
