from myrtle.console import console
from typing import Tuple
import time
import requests
from huggingface_hub import snapshot_download
import os


def download_model(model):
    snapshot_download(model)


def download_file(url: dict, filetype: str = "bz2") -> Tuple[str, str]:
    """
    Downloads a file from the specified URL and saves it locally.

    Args:
        url (dict): Contains the url as string ("url") and associated id ("id") for the file to be downloaded.
        filetype (str, optional): The file type extension. Defaults to "bz2".

    Returns:
        Tuple[str, str]: A tuple containing the file path and the identifier of the downloaded file.
    """
    console.log(f"Starting download for {url['id']}")
    with requests.get(url["url"], stream=True) as raw:
        total_length = int(raw.headers.get("Content-Length"))
        directory = "./data"
        if not os.path.exists(directory):
            os.makedirs(directory)
        filepath = f"{directory}/{os.path.basename(url['id'])}.{filetype}"

        with open(filepath, "wb") as output:
            start_time = time.time()
            update_time = start_time + 10
            for chunk in raw:
                output.write(chunk)
                if time.time() >= update_time:
                    elapsed_time = time.time() - start_time
                    downloaded = output.tell()
                    speed = downloaded / elapsed_time
                    progress = min(downloaded / total_length, 1.0) * 100
                    console.log(f"ID: {url['id']} Progress: {progress:.2f}%, Speed: {speed:.2f} B/s")
                    update_time += 10
    return filepath, url["id"]
