import os
import gzip
import math
import re
import pandas as pd
from myrtle.console import console
from fuzzywuzzy import fuzz
import time
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

    console.log("Reading csv")
    names = []
    batch_size = 100000
    chunk_counter = 0
    total_chunks = math.ceil(sum(1 for _ in open(csv_path)) / batch_size)
    for df_chunk in pd.read_csv(csv_path, chunksize=batch_size):
        chunk_counter += 1
        print(f"Processing chunk {chunk_counter} of {total_chunks}")

        df_chunk = df_chunk[df_chunk["gender"] != "Male"]
        df_chunk["name"] = df_chunk["name"].apply(lambda x: re.sub(r"\([^)]*\)", "", x))
        df_chunk["name"] = df_chunk["name"].apply(lambda x: x.replace("_", " ").lower())
        names.extend(df_chunk["name"].unique().tolist())

    console.log("Reading csv finished")

    return names


def get_split_quotes(num_processes=10) -> list:
    dl_path, id_ = download_file(
        {
            "url": "https://huggingface.co/datasets/jstet/quotes-500k/resolve/main/quotes.csv",
            "id": "jstet/quotes-500k",
        },
        "csv",
    )

    df = pd.read_csv(dl_path)

    chunk_size = len(df) // num_processes
    chunks = [df[i * chunk_size : (i + 1) * chunk_size] for i in range(num_processes)]

    os.remove(dl_path)

    return chunks


def filter_author(tuple, names, total):
    threshold = 94
    if tuple[1] % 100 == 0:
        console.log(f"row {tuple[1]} of {total}")
    # "Christian D. Larson, Your Forces and How to Use Them"
    if isinstance(tuple[0], str):
        author = tuple[0].split(",")[0]
        for name in names:
            if fuzz.ratio(author.lower(), name.lower()) >= threshold:
                return True
    return False


def filter_quotes(chunk, names):
    start_time = time.time()
    chunk = chunk.dropna(subset=["category"])
    chunk = chunk[chunk["category"].str.contains("inspirational")]
    chunk = chunk.reset_index(drop=True)
    total = len(chunk)
    chunk["keep_row"] = [filter_author(x, names, total) for x in zip(chunk["author"], chunk.index)]
    chunk = chunk[chunk["keep_row"]]
    if "keep_row" in chunk:
        chunk = chunk.drop("keep_row", axis=1)

    end_time = time.time()
    execution_time = end_time - start_time
    console.log(f"Execution time: {execution_time} seconds for {total} rows")
    return chunk
