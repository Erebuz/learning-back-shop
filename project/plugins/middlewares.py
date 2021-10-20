from secure import Secure

secure_headers = Secure()


def setup_middlewares(app):
    @app.middleware('response')
    async def set_secure_headers(request, response):
        secure_headers.framework.sanic(response)
