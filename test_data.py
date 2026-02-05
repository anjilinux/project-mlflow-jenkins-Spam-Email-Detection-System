import pandas as pd

def test_data_loading():
    df = pd.read_csv("data/raw/spam.csv")
    assert not df.empty
    assert "label" in df.columns
    assert "text" in df.columns
