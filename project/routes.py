from sanic.response import text

from project.db.handler import DBHandler


def setup_routes(app):
    # @app.route("/", methods=["GET"])
    # async def general(request):
    #     return response.json(status=200, body={"name": "general"})

    # @app.route("/admin")
    # @protected()
    # @scoped("admin")
    # async def admin(request, *args, **kwargs):
    #     return json(status=200, body={"name": "admin"})
    #
    # @app.route("/user")
    # @protected()
    # @scoped(["user", "admin"], False)
    # async def user(request, *args, **kwargs):
    #     return json(status=200, body={"name": "user"})

    @app.route("/reg/user", methods=["POST"])
    async def reg_user(req):
        message = req.json

        if message['mail'] == "" or message['password'] == "":
            return text(status=400, body="Missing password or login")

        db = DBHandler()
        db.set_new_user(message)
        del db

        return text(status=200, body="OK")
