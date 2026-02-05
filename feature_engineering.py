# src/feature_engineering.py
from sklearn.feature_extraction.text import TfidfVectorizer


def vectorize(train_texts, test_texts):
vectorizer = TfidfVectorizer(stop_words='english', max_features=5000)
X_train = vectorizer.fit_transform(train_texts)
X_test = vectorizer.transform(test_texts)
return X_train, X_test, vectorizer