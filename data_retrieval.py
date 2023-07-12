from myrtle.pipelines import get_process_notable_ppl
import modal


stub = modal.Stub("myrtle_data")

image = modal.Image.debian_slim().poetry_install_from_file("pyproject.toml")


@stub.function(image=image, timeout=1000, secret=modal.Secret.from_dotenv(__file__))
def f1():
    return get_process_notable_ppl()


@stub.local_entrypoint()
def main():
    f1.call()
