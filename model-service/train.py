"""Trains a tiny sentiment classifier and saves it to disk.
Run this once locally before building the Docker image."""

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
import joblib

texts = [
    "I love this product, it works great",
    "Absolutely wonderful experience, highly recommend",
    "Best purchase I've made all year",
    "This is amazing and exceeded my expectations",
    "Great quality and fast shipping, very happy",
    "Fantastic value for the price, would buy again",
    "Superb craftsmanship, I'm thrilled with it",
    "Exceptional service, will definitely return",
    "Terrible quality, broke after one day",
    "Worst customer service I've ever had",
    "Complete waste of money, do not buy",
    "Awful experience, very disappointed",
    "This is terrible and awful, total letdown",
    "Poor quality and slow shipping, very unhappy",
    "Horrible product, completely useless",
    "Extremely dissatisfied, would not recommend",
]
labels = [1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0]

pipeline = Pipeline([
    ("tfidf", TfidfVectorizer()),
    ("clf", LogisticRegression()),
])
pipeline.fit(texts, labels)

joblib.dump(pipeline, "model.joblib")
print("Saved model.joblib")