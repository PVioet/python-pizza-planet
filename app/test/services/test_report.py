import pytest


def test_generate_report_service(generate_report):
    report = generate_report.json
    pytest.assume(generate_report.status.startswith('200'))
    pytest.assume(report['ingredient'])
    pytest.assume(report['beverage'])
    pytest.assume(report['month'])
    pytest.assume(report['customers'])
