from app.common.http_methods import GET
from flask import Blueprint

from .base import BaseService
from ..controllers import ReportController

report = Blueprint('report', __name__)
report_service = BaseService(ReportController)


@report.route('/', methods=GET)
def generate_report():
    return report_service.generate()
