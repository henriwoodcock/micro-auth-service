import logging
from http import HTTPStatus
from datetime import datetime, timedelta
from uuid import uuid4

from flask import request, current_app, g
import jwt

from auth_service.database import db
from auth_service.common import db_wrapper
from auth_service import authentication

_logger = logging.getLogger(__name__)


def status_check():
    return {'version': '1.0.0'}, HTTPStatus.OK


@authentication.auth_required
def auth_check():
    with db.session() as session:
        res = session.execute(
            'select username from users where uuid = :uuid',
            params={'uuid': g.user_uuid}
        ).one_or_none()
    if res is None:
        return {}, HTTPStatus.UNAUTHORIZED

    return {'message': f'Hello {res.username}'}, HTTPStatus.OK


def signup():
    data = request.get_json()
    username = data['username']
    password = data['password']
    uuid = uuid4().hex
    with db.session() as session:
        try:
            db_wrapper.create_user(session, username, password, uuid)
            session.commit()
        except Exception:
            _logger.exception('error while creating user')
            session.rollback()
            return {'status': 'ERROR'}, HTTPStatus.INTERNAL_SERVER_ERROR

    return {}, HTTPStatus.OK


def login():
    data = request.get_json()
    username = data['username']
    password = data['password']
    config = current_app.config

    with db.session() as session:
        try:
            user = db_wrapper.retrieve_user(session, username)
        except Exception:
            _logger.exception('error while fetching user')
            session.rollback()
            return {'status': 'ERROR'}, HTTPStatus.INTERNAL_SERVER_ERROR

    if user is None:
        return {'status': 'USER_NOT_FOUND'}, HTTPStatus.NOT_FOUND

    # check password
    assert password == user.password

    payload = {
        'user_uuid': user.uuid,
        'exp': datetime.utcnow() + timedelta(
            seconds=config['JWT_EXP_DELTA_SECONDS']
        )
    }
    jwt_token = jwt.encode(
        payload, config['JWT_SECRET'], config['JWT_ALGORITHM']
    )

    return {'token': jwt_token}, HTTPStatus.OK
