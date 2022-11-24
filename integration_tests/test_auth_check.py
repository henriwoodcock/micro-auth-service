from http import HTTPStatus


def test_round_trip(app_client):
    resp = app_client.get('/auth-check')
    assert resp.status_code == HTTPStatus.OK
    assert resp.json() == {'message': 'Hello bobby', 'status': 'OK'}
