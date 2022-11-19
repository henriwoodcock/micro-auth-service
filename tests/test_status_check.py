from http import HTTPStatus


def test_status_check(app_client):
    resp = app_client.get('/status-check')
    assert resp.status_code == HTTPStatus.OK
    assert resp.json == {'version': '1.0.0'}
