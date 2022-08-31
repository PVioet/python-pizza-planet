import os
import tempfile

import pytest
from app import create_app, register_blueprints
from app.plugins import db, ma
# flake8: noqa
from app.repositories.models import Beverage, Ingredient, Order, OrderDetail, Size

from .fixtures.beverage import *
from .fixtures.ingredient import *
from .fixtures.order import *
from .fixtures.size import *


@pytest.fixture
def app():

    db_fd, dbpath = tempfile.mkstemp()

    class Config:
        SQLALCHEMY_DATABASE_URI = 'sqlite:///{}'.format(dbpath)
        TESTING = True
        SQLALCHEMY_TRACK_MODIFICATIONS = False

    flask_app = create_app(Config)
    register_blueprints(flask_app)
    flask_app.app_context().push()
    db.init_app(flask_app)
    ma.init_app(flask_app)

    db.create_all()

    yield flask_app

    db.session.remove()
    db.drop_all()
    os.close(db_fd)
    os.remove(dbpath)


@pytest.fixture
def client(app):
    client = app.test_client()
    return client
