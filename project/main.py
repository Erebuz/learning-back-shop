from environs import Env
from sanic import Sanic
from sanic_cors import CORS

from project.plugins import jwtPlugin
from project.plugins.middlewares import setup_middlewares
from project.routes import setup_routes
from project.settings import Settings


class App:
    def __init__(self):
        app = Sanic(__name__)
        app.config.update(Settings)

        jwtPlugin.setup_jwt(app)
        CORS(app)

        env = Env()
        env.read_env()

        setup_routes(app)
        setup_middlewares(app)

        app.run(
            host=app.config.HOST,
            port=app.config.PORT,
            debug=app.config.DEBUG,
            auto_reload=app.config.DEBUG,
        )
