from http import HTTPStatus


def test_signup(app_client, db_session):
    resp = app_client.post(
        '/signup', json={'username': 'bobby', 'password': 'password'}
    )
    assert resp.status_code == HTTPStatus.OK

    user = db_session.execute(
        'select username from users where username = :username',
        params={'username': 'bobby'}
    ).one_or_none()
    assert user is not None
