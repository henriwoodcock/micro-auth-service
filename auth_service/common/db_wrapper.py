def create_user(session, username: str, password: str, uuid: str):
    session.execute(
        """
            INSERT INTO USERS (username, password, uuid)
            VALUES (:username, :password, :uuid)
        """,
        params={
            'username': username,
            'password': password,
            'uuid': uuid
        }
    )


def retrieve_user(session, username):
    return session.execute(
      """
          SELECT
              username,
              password,
              uuid
          FROM
              users
          WHERE
              username = :username
      """,
      params={'username': username}
    ).one_or_none()
