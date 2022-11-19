from http import HTTPStatus


def test_round_trip(app_client):
    resp = app_client.post(
        '/signup', json={'username': 'bobby', 'password': 'password'}
    )
    assert resp.status_code == HTTPStatus.OK

    resp = app_client.post(
        '/login', json={'username': 'bobby', 'password': 'password'}
    )
    assert resp.status_code == HTTPStatus.OK
    token = resp.json['token']

    resp = app_client.get(
        'auth-check', headers={'Authorization': f'Bearer {token}'}
    )
    assert resp.status_code == HTTPStatus.OK
    assert resp.json == {'message': 'Hello bobby'}
