import os
import gzip
import pandas as pd
from myrtle.helpers import download_file


def get_process_notable_ppl() -> list:
    csv_path = "./data/notable_people.csv"

    if not os.path.exists(csv_path):
        gz_path, id_ = download_file(
            {
                "url": "https://huggingface.co/datasets/jstet/laouenan-notable-people/resolve/main/cross-verified-database.csv.gz",
                "id": "jstet/laouenan-notable-people",
            },
            "gz",
        )

        with open(gz_path, "rb") as inf, open(csv_path, "w", encoding="utf-8") as tof:
            decom_str = gzip.decompress(inf.read()).decode("utf-8", errors="replace")
            tof.write(decom_str)

        os.remove(gz_path)

    # Read the CSV content into a DataFrame
    df = pd.read_csv(csv_path)

    df = df[df["gender"] != "Male"]

    df["name"] = df["name"].apply(lambda x: x.replace("_", " "))

    names_lst = df["name"].unique().tolist()

    return names_lst
