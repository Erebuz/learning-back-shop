from sanic.response import text, json
from sanic_jwt import protected, scoped, inject_user

from project.db.handler import DBHandler


def setup_routes(app):
    @app.route("/reg/admin", methods=["POST"])
    @protected()
    @scoped(["admin"], False)
    async def reg_admin(req):
        message = req.json

        if message['login'] == "" or message['password'] == "":
            return text(status=400, body="Missing password or login")

        db = DBHandler()
        db.set_new_user(message, 1)
        del db

        return text(status=200, body="OK")

    @app.route("/reg/owner", methods=["POST"])
    @protected()
    @scoped(["admin"], False)
    async def reg_owner(req):
        message = req.json

        if message['login'] == "" or message['password'] == "":
            return text(status=400, body="Missing password or login")

        db = DBHandler()
        db.set_new_user(message, 2)
        del db

        return text(status=200, body="OK")

    @app.route("/reg/seller", methods=["POST"])
    @protected()
    @scoped(["admin", "owner"], False)
    async def reg_seller(req):
        message = req.json

        if message['login'] == "" or message['password'] == "":
            return text(status=400, body="Missing password or login")

        db = DBHandler()
        db.set_new_user(message, 3)
        del db

        return text(status=200, body="OK")

    @app.route("/reg/user", methods=["POST"])
    async def reg_user(req):
        message = req.json

        if message['login'] == "" or message['password'] == "":
            return text(status=400, body="Missing password or login")

        db = DBHandler()
        db.set_new_user(message, 4)
        del db

        return text(status=200, body="OK")

    @app.route("/get_user_data", methods=["GET"])
    @inject_user()
    @protected()
    async def get_user_data(req, user):
        db = DBHandler()
        data = db.get_user_data(user.user_id)
        del db

        return json(status=200, body=data)

    @app.route("/change_user_data", methods=["POST"])
    @inject_user()
    @protected()
    async def change_user_data(req, user):
        message = req.json

        if message['login'] == "" or message['password'] == "":
            return text(status=400, body="Missing password or login")

        db = DBHandler()
        db.edit_user_data(message, user.user_id)
        del db

        return text(status=200, body="OK")
