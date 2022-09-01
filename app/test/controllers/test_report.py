import pytest
from app.controllers import ReportController, OrderController


def test_generate(app, orders: list):
    for order in orders:
        _, _ = OrderController.create(order)

    created_report, error = ReportController.generate()
    pytest.assume(error is None)
    pytest.assume(created_report['ingredient'])
    pytest.assume(created_report['beverage'])
    pytest.assume(created_report['month'])
    pytest.assume(created_report['customers'])
