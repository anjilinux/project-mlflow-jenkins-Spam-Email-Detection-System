# data_ingestion.py
import pandas as pd
import os
import urllib.request
import zipfile

DATA_FILE = "spam.csv"
DATA_URL = "https://archive.ics.uci.edu/ml/machine-learning-databases/00228/smsspamcollection.zip"

def download_data():
    if os.path.exists(DATA_FILE):
        print("✅ Dataset already exists")
        return

    print("⬇️ Downloading dataset...")
    urllib.request.urlretrieve(DATA_URL, "spam.zip")

    with zipfile.ZipFile("spam.zip", "r") as z:
        z.extractall(".")

    # The extracted file is TAB-separated, no header
    df = pd.read_csv(
        "SMSSpamCollection",
        sep="\t",
        header=None,
        names=["label", "text"],
        encoding="latin-1"
    )

    df.to_csv(DATA_FILE, index=False)

    os.remove("spam.zip")
    os.remove("SMSSpamCollection")

    print("✅ spam.csv created successfully")

def load_data(path):
    if not os.path.isfile(path):
        raise FileNotFoundError(f"❌ {path} not found")
    return pd.read_csv(path)

if __name__ == "__main__":
    download_data()
    df = load_data(DATA_FILE)
    print("📊 Dataset shape:", df.shape)
    print(df.head())
