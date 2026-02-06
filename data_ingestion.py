# data_ingestion.py
import pandas as pd
import os
import urllib.request

DATA_FILE = "spam.csv"
DATA_URL = "https://archive.ics.uci.edu/ml/machine-learning-databases/00228/smsspamcollection.zip"

def load_data(path: str) -> pd.DataFrame:
    if not os.path.exists(path):
        raise FileNotFoundError(f"Data file not found at {path}")
    return pd.read_csv(path, encoding="latin-1")[["v1", "v2"]].rename(
        columns={"v1": "label", "v2": "text"}
    )

def download_data():
    if os.path.exists(DATA_FILE):
        return

    print("⬇️ Downloading dataset...")
    urllib.request.urlretrieve(DATA_URL, "spam.zip")

    import zipfile
    with zipfile.ZipFile("spam.zip", "r") as z:
        z.extractall(".")

    os.rename("SMSSpamCollection", DATA_FILE)
    os.remove("spam.zip")

if __name__ == "__main__":
    download_data()
    df = load_data(DATA_FILE)
    print(f"✅ Data ready: {df.shape}")
