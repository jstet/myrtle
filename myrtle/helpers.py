import urllib.request
import os


def download_model():
    path = "/.cache/gpt4all"
    # Check whether the specified path exists or not
    isExist = os.path.exists(path)
    if not isExist:
        os.makedirs(path)

    urllib.request.urlretrieve(
        "https://huggingface.co/TheBloke/orca_mini_3B-GGML/resolve/main/orca-mini-3b.ggmlv3.q4_0.bin",
        f"{path}/model.bin",
    )
