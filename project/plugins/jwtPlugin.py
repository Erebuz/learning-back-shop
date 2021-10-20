from sanic_jwt import initialize, exceptions

from project.bd.handler import username_table, userid_table


async def authenticate(request, *args, **kwargs):
    username = request.json.get("username", None)
    password = request.json.get("password", None)

    if not username or not password:
        raise exceptions.AuthenticationFailed("Missing username or password.")

    user = username_table.get(username, None)
    if user is None:
        raise exceptions.AuthenticationFailed("User not found.")

    if password != user.password:
        raise exceptions.AuthenticationFailed("Password is incorrect.")

    return user


async def retrieve_user(request, payload, *args, **kwargs):
    if payload:
        user_id = payload.get('user_id', None)
        user = userid_table.get(user_id, None)
        return user
    else:
        return None


async def get_user_roles(user, *args, **kwargs):
    return user.scopes


def setup_jwt(app):
    initialize(app,
               authenticate=authenticate,
               retrieve_user=retrieve_user,
               add_scopes_to_payload=get_user_roles)
