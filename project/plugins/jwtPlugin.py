from sanic_jwt import initialize, exceptions

from project.classes.User import User


users = [User(1, "admin", "admin", ['admin']), User(2, "user", "user", ["user"])]

username_table = {u.username: u for u in users}
userid_table = {u.user_id: u for u in users}


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
        user = users[0]
        return user
    else:
        return None


async def get_user_roles(user, *args, **kwargs):
    return user.scopes


def init(app):
    initialize(app,
               authenticate=authenticate,
               retrieve_user=retrieve_user,
               add_scopes_to_payload=get_user_roles)
