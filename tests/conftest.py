import testing.postgresql
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker
import pytest

from auth_service import database
from auth_service.app import create_app


@pytest.fixture
def db_session(monkeypatch):
    # Lanuch new PostgreSQL server
    with testing.postgresql.Postgresql() as postgresql:
        # connect to PostgreSQL
        engine = create_engine(postgresql.url())
        session_factory = sessionmaker(bind=engine)
        Session = scoped_session(session_factory)
        with open("db/create_schema.sql") as file:
            raw = file.read()
        Session.execute(raw)
        Session.commit()
        monkeypatch.setattr(database.db, "session", Session)

        yield Session
        Session.rollback()
        Session.close()


@pytest.fixture
def app_client(db_session):
    flask_app = create_app()
    client = flask_app.app.test_client(use_cookies=True)
    yield client
