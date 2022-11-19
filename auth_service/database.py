""" Module defining the database for the app.
"""

__all__ = ('db',)

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()  # pylint: disable=invalid-name
