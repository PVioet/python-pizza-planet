import inspect

from flask import Blueprint, Flask


def create_app(config_class: str):
    flask_app = Flask(__name__)
    flask_app.config.from_object(config_class)
    return flask_app


def register_blueprints(flask_app):
    from app import services
    blueprints = inspect.getmembers(services, lambda member: isinstance(member, Blueprint))
    for name, blueprint in blueprints:
        prefix = '/' if name == 'index' else f'/{name.replace("_", "-")}'
        flask_app.register_blueprint(blueprint, url_prefix=prefix)


def register_plugins(flask_app):
    from .plugins import db, ma
    db.init_app(flask_app)
    ma.init_app(flask_app)


def cors_app(flask_app):
    from flask_cors import CORS
    CORS(flask_app)


def configure_app(config_class):
    flask_app = create_app(config_class)
    register_blueprints(flask_app)
    register_plugins(flask_app)
    cors_app(flask_app)

    return flask_app


flask_app = configure_app('app.settings.Config')
