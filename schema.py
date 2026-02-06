# schema.py
import pandas as pd
from pydantic import BaseModel, Field


# -------- API Schemas --------

class EmailRequest(BaseModel):
    text: str = Field(..., min_length=1)


class PredictionResponse(BaseModel):
    spam: bool


# -------- Dataset Schema Validation --------

EXPECTED_COLUMNS = {"label", "text"}


def validate_schema(csv_path: str = "spam.csv") -> bool:
    """
    Validates dataset schema.
    Returns True if schema is valid, else raises ValueError.
    """
    df = pd.read_csv(csv_path)

    missing_cols = EXPECTED_COLUMNS - set(df.columns)
    if missing_cols:
        raise ValueError(f"❌ Missing columns: {missing_cols}")

    if df.empty:
        raise ValueError("❌ Dataset is empty")

    return True


# -------- CLI / Jenkins Hook --------

if __name__ == "__main__":
    try:
        validate_schema()
        print("✅ Dataset schema validation passed")
    except Exception as e:
        print(str(e))
        raise
