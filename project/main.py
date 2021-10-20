from environs import Env
from sanic import Sanic
from sanic_cors import CORS

from project.plugins.middlewares import setup_middlewares
from project.routes import setup_routes
from project.settings import Settings

from project.plugins import jwtPlugin

app = Sanic(__name__)
jwtPlugin.setup_jwt(app)
CORS(app)


def init():
    env = Env()
    env.read_env()

    app.config.update(Settings)
    setup_routes(app)
    setup_middlewares(app)

    app.run(
        host=app.config.HOST,
        port=app.config.PORT,
        debug=app.config.DEBUG,
        auto_reload=app.config.DEBUG,
    )
