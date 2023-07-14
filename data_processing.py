import pandas as pd
from autocorrect import Speller
import contractions
from myrtle.console import console
from myrtle.helpers import is_grammatically_correct
from langdetect import detect
import re
import language_tool_python

df = pd.read_csv("./data/filtered_quotes.csv")

# df["quote"] = df["quote"].str.lower()
console.log(f"{len(df)} quotes.")

console.log("Fixing contractions")
df["quote"] = df["quote"].apply(contractions.fix)

console.log("Removing HTML special entities")
df["quote"] = df["quote"].str.replace(r"&\w+;", "")

console.log("Removing extra whitespaces")
df["quote"] = df["quote"].str.replace(r"\s+", " ")

console.log("Inserting whitespaces between a word and punctuation")


def add_whitespace(s):
    return re.sub(r"(?<=[.,?!])(?=[^\s])", r" ", s)


df["quote"] = df["quote"].apply(lambda x: add_whitespace(x))
df["quote"] = df["quote"].str.replace(". . .", "...")

console.log("Removing quotes that contain ' or \"")
df = df[df["quote"].apply(lambda x: "'" not in x and '"' not in x)]
console.log(f"{len(df)} quotes left")


def keep_only_asci(x):
    RE_ASCII = re.compile(r"[^A-Za-zÀ-ž,.!?0-9 ;:]", re.IGNORECASE)
    x = re.sub(RE_ASCII, " ", x)
    return x


console.log("Keep only ASCII characters (also remove quotation)")
df["quote"] = df["quote"].apply(keep_only_asci)


console.log("Remove ... at beginning of quotes and convert first character to uppercase")
df["quote"] = df["quote"].apply(lambda x: x.replace("...", "") if x.startswith("...") else x)
df["quote"] = df["quote"].apply(lambda x: x[0].upper() + x[1:])

console.log("Remove trailing whitespace")
df["quote"] = df["quote"].str.strip()

console.log("Add a dot at end of quote if it doesnt end with dot or similar already")
df["quote"] = df["quote"].apply(
    lambda x: x + "." if not x.endswith(".") and not x.endswith("!") and not x.endswith("?") else x
)

console.log("Remove  whitespace. at end of quotes")
df["quote"] = df["quote"].apply(lambda x: x.replace(" .", "") if x.endswith(" .") else x)

console.log("Removing quotes with less or equal to 100 words")
df = df[df["quote"].apply(lambda x: len(x.split()) <= 100)]
console.log(f"{len(df)} quotes left")

console.log("remove a quote if it is not english with langdetect")
df = df[df["quote"].apply(lambda x: detect(x) == "en")]
console.log(f"{len(df)} quotes left")

spell = Speller()

console.log("Spelling correction")
df["quote"] = df["quote"].apply(spell)

tool = language_tool_python.LanguageTool("en-US")

console.log("remove a quote if it is not grammatically correct")
df = df[[is_grammatically_correct(x, tool, 1) for x in df["quote"]]]
console.log(f"{len(df)} quotes left")

df = df["quote"]

df.to_csv("./data/processed/processed_quotes.csv", index=False)
