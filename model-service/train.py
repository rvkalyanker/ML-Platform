"""Trains a tiny sentiment classifier and saves it to disk.
Run this once locally before building the Docker image."""

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
import joblib

# Small illustrative dataset — swap for something larger later if you want.
texts = [ "I love this product, it works great", 
"Absolutely wonderful experience, highly recommend", 
"Best purchase I've made all year", 
"This is amazing and exceeded my expectations", 
"Great quality and fast shipping, very happy", 
"Fantastic value for the price, would buy again", 
"Terrible quality, broke after one day", 
"Worst customer service I've ever had", 
"Complete waste of money, do not buy", 
"Awful experience, very disappointed", 
"This is terrible and awful, total letdown", 
"Poor quality and slow shipping, very unhappy",] 

labels = [1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0] # 1 = positive, 0 = negative

pipeline = Pipeline([
    ("tfidf", TfidfVectorizer()),
    ("clf", LogisticRegression()),
])
pipeline.fit(texts, labels)

joblib.dump(pipeline, "model.joblib")
print("Saved model.joblib")