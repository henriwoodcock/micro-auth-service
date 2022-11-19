from http import HTTPStatus

from flask import request, current_app, g
import jwt


def auth_required(func):
    def inner(*args, **kwargs):
        jwt_token = request.headers.get('authorization', None)
        config = current_app.config
        JWT_SECRET = config['JWT_SECRET']
        JWT_ALGORITHM = config['JWT_ALGORITHM']

        if jwt_token is None:
            return {'status': 'NO_TOKEN'}, HTTPStatus.UNAUTHORIZED

        try:
            bearer = jwt_token.split('Bearer ')[1]
        except IndexError:
            return {'status': 'INVALID_FORMAT'}, HTTPStatus.UNAUTHORIZED
        try:
            payload = jwt.decode(
                bearer, JWT_SECRET, algorithms=[JWT_ALGORITHM]
            )
        except (jwt.DecodeError, jwt.ExpiredSignatureError):
            return {'message': 'Token is invalid'}, HTTPStatus.UNAUTHORIZED

        g.user_uuid = payload['user_uuid']
        return func(*args, **kwargs)
    return inner
