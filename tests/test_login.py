import datetime
from http import HTTPStatus

import pytest

from auth_service import routes


@pytest.fixture
def fake_user(db_session):
    uuid = 'ac465bbd2aee4bf785e670895e552560'
    db_session.execute(
        """
            insert into users (username, password, uuid)
            values (:username, :password, :uuid)
        """,
        params={'username': 'bobby', 'password': 'bad-pass', 'uuid': uuid}
    )
    db_session.commit()
    yield


class fakedatetime:
    def utcnow(self):
        return datetime.datetime(2022, 1, 1)


def test_login(monkeypatch, app_client, fake_user):
    monkeypatch.setattr(routes, 'datetime', fakedatetime())
    monkeypatch.setattr(
        routes, 'timedelta', lambda seconds: datetime.timedelta(seconds=0)
    )
    resp = app_client.post(
        '/login', json={'username': 'bobby', 'password': 'bad-pass'}
    )
    assert resp.status_code == HTTPStatus.OK
    assert resp.json == {
      'token': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX3V1aWQ'
               'iOiJhYzQ2NWJiZDJhZWU0YmY3ODVlNjcwODk1ZTU1MjU2MCIsImV'
               '4cCI6MTY0MDk5NTIwMH0.YrrZpFAuCCbcXW5TzkK407EjAuWQvfQ'
               'Q_6HGUJJDT2c'
    }
