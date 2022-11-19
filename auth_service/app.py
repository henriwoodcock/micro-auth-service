import logging
import pathlib

import yaml
import connexion

from auth_service import database

__all__ = (
    "create_app",
)

_logger = logging.getLogger(__name__)


def load_config():
    with open(pathlib.Path('auth_service/config.yml'), 'r') as f:
        config = yaml.safe_load(f)
    return config


def create_app():
    config = load_config()
    app_name = config['app_name']
    _logger.info(f'Creating {app_name} app')

    flask_app = connexion.FlaskApp(app_name, specification_dir='./')
    flask_app.add_api('auth_service/api.yml')
    flask_app.app.config.update(
        {'SQLALCHEMY_DATABASE_URI': config['DB_URI']}
    )
    flask_app.app.config.update(config)

    database.db.init_app(flask_app.app)

    _logger.debug("App creation completed.")
    return flask_app
