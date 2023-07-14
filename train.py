import os
from dotenv import load_dotenv
from modal import Image, Stub, Mount, Secret
from myrtle.training import finetune

load_dotenv()

image = (
    Image.debian_slim()
    .poetry_install_from_file("pyproject.toml")
    .apt_install(["git", "git-lfs"])
    .run_commands("git lfs install")
)

stub = Stub(name="myrtle_train", image=image)

csv_dir = "./data/processed"


@stub.function(
    gpu="A10g",
    timeout=7200,
    mounts=[Mount.from_local_dir(csv_dir, remote_path=f"/root/{csv_dir}")],
    secret=Secret.from_dotenv(__file__),
)
def f1():
    token = os.environ.get("HF_TOKEN")
    finetune(f"{csv_dir}/processed_quotes.csv", token)
