import pandas as pd
from sklearn.model_selection import train_test_split


def preprocess_and_split(df, test_size=0.2, random_state=42):
    """
    Split spam dataset into train/test sets
    """

    # Basic validation
    if "text" not in df.columns or "label" not in df.columns:
        raise ValueError("Dataset must contain 'text' and 'label' columns")

    X = df["text"]
    y = df["label"]

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=test_size,
        random_state=random_state,
        stratify=y
    )

    return X_train, X_test, y_train, y_test


if __name__ == "__main__":
    print("✅ Data preprocessing module loaded")
