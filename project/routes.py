from sanic.response import text, json, raw
from sanic_jwt import protected, scoped, inject_user
import base64
from urllib.parse import unquote

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

        if message['login'] == "":
            return text(status=400, body="Missing login")

        db = DBHandler()
        db.edit_user_data(message, user.user_id)
        del db

        return text(status=200, body="OK")

    @app.route("/product/all", methods=["GET"])
    async def get_product_all(req):
        db = DBHandler()
        data = db.get_product_all()
        del db
        print(data)
        return json(status=200, body=data)

    @app.route("/product/image/<pr_type>/<path>", methods=["GET"])
    async def get_image(req, pr_type, path):
        try:
            image = open("../images/{}/{}".format(unquote(pr_type), unquote(path)), "rb")
            img64 = base64.b64encode(image.read())
        except Exception as err:
            return text(status=400, body="Image not found")
        else:
            return raw(img64, content_type='image/jpeg')

    @app.route("/order/create", methods=["POST"])
    async def create_simple_order(req):
        db = DBHandler()

        user = {"phone_number": req.json["phone"]}
        data = db.get_simple_user(user, 5)

        db.create_new_order(data, req.json["basket"])

        del db

        return text(status=200, body="OK")

    @app.route("/order/create_auth", methods=["POST"])
    @inject_user()
    @protected()
    async def create_order(req, user):
        db = DBHandler()
        db.create_new_order(user.user_id, req.json["basket"])
        del db
        return text(status=200, body="OK")

    @app.route("/order/history", methods=["GET"])
    @inject_user()
    @protected()
    async def get_history(req, user):
        db = DBHandler()
        data = db.get_client_history(user.user_id)
        del db
        return json(status=200, body=data)
