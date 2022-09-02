from app.common.http_methods import GET, POST, PUT
from flask import Blueprint

from .base import BaseService
from ..controllers import BeverageController

beverage = Blueprint('beverage', __name__)
beverage_service = BaseService(BeverageController)


@beverage.route('/', methods=POST)
def create_beverage():
    return beverage_service.create()


@beverage.route('/', methods=PUT)
def update_beverage():
    return beverage_service.update()


@beverage.route('/id/<_id>', methods=GET)
def get_beverage_by_id(_id: int):
    return beverage_service.get_by_id(_id)


@beverage.route('/', methods=GET)
def get_beverages():
    return beverage_service.get_all()
