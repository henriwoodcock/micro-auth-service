from http import HTTPStatus
import time

import pytest
import requests


class AuthClient:
    def __init__(self):
        self.url = 'http://localhost:5000'
        self.headers = {}

    def login(self, username: str, password: str):
        resp = requests.post(
          f'{self.url}/login',
          json={'username': username, 'password': password}
        )
        if resp.status_code != HTTPStatus.OK:
            raise Exception(f'Failed to login, {resp.json()}')
        self.headers['Authorization'] = f'Bearer {resp.json()["token"]}'

    def signup(self, username: str, password: str):
        resp = requests.post(
          f'{self.url}/signup',
          json={'username': username, 'password': password}
        )
        if resp.status_code != HTTPStatus.OK:
            raise Exception(f'Failed to login, {resp.json()}')

    def get(self, url, *args, **kwargs):
        return requests.get(
            f'{self.url}{url}', *args, **kwargs, headers=self.headers
        )

    def post(self, url, *args, **kwargs):
        return requests.post(
            f'{self.url}{url}', *args, **kwargs, headers=self.headers
        )

    def delete(self, url, *args, **kwargs):
        return requests.delete(
            f'{self.url}{url}', *args, **kwargs, headers=self.headers
        )


@pytest.fixture(scope='session')
def _app_client():
    max_tries = 10
    auth_client = AuthClient()
    up = False
    while not up and max_tries >= 0:
        resp = auth_client.get('/status-check')
        up = resp.status_code == HTTPStatus.OK
        if not up:
            time.sleep(10)
            max_tries -= 1
    if not up:
        raise Exception('Failed to load client')
    yield auth_client


@pytest.fixture(scope='session')
def user(_app_client):
    username = 'bobby'
    password = 'mypassword'
    _app_client.signup(username, password)
    _app_client.login(username, password)
    return username, password


@pytest.fixture(scope='session')
def app_client(_app_client, user):
    yield _app_client
    _app_client.delete('/user')
