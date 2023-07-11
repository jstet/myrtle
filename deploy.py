from myrtle.main import app

from modal import Image, Stub, asgi_app


stub = Stub("example-fastapi-app")
image = Image.debian_slim().poetry_install_from_file("pyproject.toml")


@stub.function(image=image)
@asgi_app()
def fastapi_app():
    return app
