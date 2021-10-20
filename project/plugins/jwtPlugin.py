from sanic_jwt import initialize, exceptions

from project.db.handler import DBHandler


async def authenticate(request, *args, **kwargs):
    db = DBHandler()
    username = request.json.get("username", None)
    password = request.json.get("password", None)
    user = db.get_user_by_username(username)

    del db

    if not username or not password:
        raise exceptions.AuthenticationFailed("Missing username or password.")

    if (user is None) or (password != user.password):
        raise exceptions.AuthenticationFailed("Authorization failed")

    return user


async def retrieve_user(request, payload, *args, **kwargs):
    if payload:
        db = DBHandler()
        user_id = payload.get('user_id', None)
        user = db.get_user_by_user_id(user_id)
        del db
        return user
    else:
        return None


async def get_user_roles(user, *args, **kwargs):
    return user.roles


def setup_jwt(app):
    initialize(app,
               authenticate=authenticate,
               retrieve_user=retrieve_user,
               add_scopes_to_payload=get_user_roles)
