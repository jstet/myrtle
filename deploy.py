from myrtle.main import app
from myrtle.helpers import download_model

from modal import Image, Stub, asgi_app

stub = Stub("example-fastapi-app")

image = Image.debian_slim().poetry_install_from_file("pyproject.toml").run_function(download_model)


@stub.function(image=image)
@asgi_app()
def fastapi_app():
    return app
