import sys
import time
import wikipediaapi
from pathlib import Path
import pandas as pd
import re
from tqdm import tqdm

df = pd.read_csv("data/filtered.csv")

df["products"] = df["products"].apply(lambda x: re.sub(r"\d+", "", str(x)))
words = [word for row in df['products'] for word in row.split(" ")]
subjects = list(set(words))
subjects = [x for x in subjects if x]

wiki = wikipediaapi.Wikipedia(
        language='en',
        extract_format=wikipediaapi.ExtractFormat.WIKI
)

Path("../corpus").mkdir(parents=True, exist_ok=True)
print(len(subjects))
text = ""
for i in tqdm(subjects):
    print(i)
    page_title = i
    page = wiki.page(page_title)

    try:
        text = page.text
    except KeyError:
        continue

    # Clean the text, remove any irrelevant information or formatting
    text += text.lower()
    text += text.replace("\n", " ")
    text += text.replace(".", "")
    text += text.replace(",", "")
    text += text.replace("!", "")
    text += text.replace("?", "")
    text += text.replace("-", " ")

    time.sleep(0.3)

# Store the cleaned text in a file, which can then be used as a corpus for FastText
with open(f"custom_corpus.txt", "w", encoding="utf-8") as f:
    f.write(text)
