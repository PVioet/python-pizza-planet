import pytest


def test_generate_report_service(client, report_uri):
    response = client.get(report_uri)
    pytest.assume(response.status.startswith('200'))
    report = response.json
    pytest.assume(report['ingredient'])
    pytest.assume(report['beverage'])
    pytest.assume(report['month'])
    pytest.assume(report['customers'])
