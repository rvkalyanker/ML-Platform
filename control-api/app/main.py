from fastapi import FastAPI
from app.db.session import Base, engine
from app.db import models  # noqa: F401
from app.routers import models as models_router
from app.routers import deployments as deployments_router

app = FastAPI(title="Control API")


@app.on_event("startup")
def startup_event():
    Base.metadata.create_all(bind=engine)


app.include_router(models_router.router)
app.include_router(deployments_router.router)


@app.get("/health")
def health():
    return {"status": "alive"}