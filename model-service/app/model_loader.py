import joblib
from pathlib import Path

MODEL_PATH = Path(__file__).parent.parent / "model.joblib"

_model = None  # loaded lazily, cached at module level


def load_model():
    global _model
    if _model is None:
        _model = joblib.load(MODEL_PATH)
    return _model


def is_model_loaded() -> bool:
    return _model is not None


def predict(text: str) -> dict:
    model = load_model()
    prediction = model.predict([text])[0]
    confidence = model.predict_proba([text]).max()
    return {
        "label": "positive" if prediction == 1 else "negative",
        "confidence": round(float(confidence), 4),
    }