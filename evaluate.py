from sklearn.metrics import classification_report


def evaluate(y_true, y_pred):
    """
    Generate classification report for spam model
    """
    return classification_report(y_true, y_pred)


if __name__ == "__main__":
    print("✅ Evaluation module loaded")
