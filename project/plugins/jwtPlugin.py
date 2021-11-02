from hashlib import sha256

from sanic_jwt import initialize, exceptions

from project.db.handler import DBHandler


async def authenticate(request, *args, **kwargs):
    db = DBHandler()
    username = request.json.get("username", None)
    password = sha256(bytes(request.json.get("password", None), encoding="utf-8")).hexdigest()

    user = db.get_user_by_username(username)

    del db

    if not username or not password:
        raise exceptions.AuthenticationFailed("Missing username or password.")

    if (user is None) or (password != user.pass_hash):
        raise exceptions.AuthenticationFailed("Authorization failed")

    return user


async def retrieve_user(request, payload, *args, **kwargs):
    if payload:
        db = DBHandler()
        user_id = payload.get('user_id', None)
        if user_id is None:
            return None

        user = db.get_user_auth(user_id)
        del db
        return user
    else:
        return None


async def get_user_roles(user, *args, **kwargs):
    return user.roles


def store_refresh_token(user_id, refresh_token, *args, **kwargs):
    db = DBHandler()
    db.store_refresh_token(user_id, refresh_token)
    del db


def retrieve_refresh_token(request, user_id, *args, **kwargs):
    db = DBHandler()
    token = db.get_refresh_token_by_user_id(user_id)
    del db
    print("get refresh token = {}".format(token))
    return token


def setup_jwt(app):
    initialize(app,
               authenticate=authenticate,
               retrieve_user=retrieve_user,
               add_scopes_to_payload=get_user_roles,
               secret="serenity",
               refresh_token_enabled=True,
               store_refresh_token=store_refresh_token,
               retrieve_refresh_token=retrieve_refresh_token
               )
