import pytest
from app.controllers import ReportController


def test_generate(app):
    created_report, error = ReportController.generate()
    pytest.assume(error is None)
    pytest.assume(created_report['ingredient'])
    pytest.assume(created_report['beverage'])
    pytest.assume(created_report['month'])
    pytest.assume(created_report['customers'])
