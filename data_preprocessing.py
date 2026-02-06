import pandas as pd
from sklearn.model_selection import train_test_split

from preprocessing import clean_text


def split_and_preprocess(
    df: pd.DataFrame,
    test_size: float = 0.2,
    random_state: int = 42,
):
    """
    Cleans text and splits data into train/test sets
    """

    df = df.copy()

    # Expected schema: label, text
    df["text"] = df["text"].apply(clean_text)

    X = df["text"]
    y = df["label"]

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=test_size,
        random_state=random_state,
        stratify=y,
    )

    return X_train, X_test, y_train, y_test
