import time
from fastapi import FastAPI
from pydantic import BaseModel
from app.model_loader import load_model, is_model_loaded, predict

app = FastAPI(title="Model Service")

MODEL_VERSION = "v1"


@app.on_event("startup")
def startup_event():
    # Load the model into memory once, at startup — not per-request.
    load_model()


class PredictRequest(BaseModel):
    text: str


class PredictResponse(BaseModel):
    label: str
    confidence: float
    model_version: str
    latency_ms: float


@app.post("/predict", response_model=PredictResponse)
def predict_endpoint(request: PredictRequest):
    start = time.perf_counter()
    result = predict(request.text)
    latency_ms = (time.perf_counter() - start) * 1000
    return PredictResponse(
        label=result["label"],
        confidence=result["confidence"],
        model_version=MODEL_VERSION,
        latency_ms=round(latency_ms, 2),
    )


@app.get("/health")
def health():
    # Liveness: is the process alive? Always true if we can respond at all.
    return {"status": "alive"}


@app.get("/ready")
def ready():
    # Readiness: has the model finished loading?
    if is_model_loaded():
        return {"status": "ready"}
    return {"status": "not ready"}, 503

