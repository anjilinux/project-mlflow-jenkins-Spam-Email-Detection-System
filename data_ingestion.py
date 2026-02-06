# data_ingestion.py
import pandas as pd
import os
import urllib.request
import zipfile

DATA_FILE = "spam.csv"
DATA_URL = "https://archive.ics.uci.edu/ml/machine-learning-databases/00228/smsspamcollection.zip"

def download_and_prepare():
    print("⬇️ Preparing dataset (fresh)...")

    # Clean old files
    for f in ["spam.zip", "SMSSpamCollection", DATA_FILE]:
        if os.path.exists(f):
            os.remove(f)

    urllib.request.urlretrieve(DATA_URL, "spam.zip")

    with zipfile.ZipFile("spam.zip", "r") as z:
        z.extractall(".")

    # Properly parse TAB-separated raw data
    df = pd.read_csv(
        "SMSSpamCollection",
        sep="\t",
        header=None,
        names=["label", "text"],
        encoding="latin-1"
    )

    # Write a CLEAN CSV (quoted text)
    df.to_csv(DATA_FILE, index=False)

    os.remove("spam.zip")
    os.remove("SMSSpamCollection")

    print("✅ Fresh spam.csv created")

def load_data(path):
    return pd.read_csv(path)

if __name__ == "__main__":
    download_and_prepare()
    df = load_data(DATA_FILE)
    print("📊 Dataset shape:", df.shape)
    print(df.head())
