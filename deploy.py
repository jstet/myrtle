from modal import Image, Stub, asgi_app
from myrtle.main import app

stub = Stub()

image = Image.debian_slim().poetry_install_from_file("pyproject.toml", only=["main"])


@stub.function(image=image)
@asgi_app()
def fastapi_app():
    return app
