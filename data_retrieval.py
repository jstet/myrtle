from myrtle.pipelines import get_process_notable_ppl, get_split_quotes, filter_quotes
import modal
from myrtle.console import console
import pandas as pd


stub = modal.Stub("myrtle_data")

image = modal.Image.debian_slim().poetry_install_from_file("pyproject.toml")


@stub.function(image=image, timeout=8000, secret=modal.Secret.from_dotenv(__file__))
def f3(chunk, names):
    return filter_quotes(chunk, names)


@stub.local_entrypoint()
def main():
    notable = get_process_notable_ppl()
    string = "\n".join(notable)
    with open("./data/notable.csv", "w") as file:
        file.write(string)

    chunks = get_split_quotes(30)
    lst = []
    console.log("Starting to filter..")
    for chunk in f3.map(chunks, kwargs={"names": notable}):
        lst.append(chunk)

    filtered_quotes_df = pd.concat(lst)

    filtered_quotes_df.to_csv("./data/filtered_quotes.csv", index=False)
