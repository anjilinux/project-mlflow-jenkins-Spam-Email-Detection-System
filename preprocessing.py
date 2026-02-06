import re


def clean_text(text: str) -> str:
    """
    Basic text cleaning for spam detection
    """
    if not isinstance(text, str):
        return ""

    text = text.lower()
    text = re.sub(r"http\S+", " ", text)        # remove URLs
    text = re.sub(r"\W+", " ", text)             # remove special chars
    text = re.sub(r"\s+", " ", text).strip()     # remove extra spaces

    return text
