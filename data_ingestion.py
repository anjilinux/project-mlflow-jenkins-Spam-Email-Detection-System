# data_ingestion.py
import pandas as pd
import os

def load_data(path: str) -> pd.DataFrame:
    if not os.path.exists(path):
        raise FileNotFoundError(f"Data file not found at {path}")
    return pd.read_csv(path)

if __name__ == "__main__":
    df = load_data("spam.csv")
    print(f"Data loaded successfully with shape: {df.shape}")
