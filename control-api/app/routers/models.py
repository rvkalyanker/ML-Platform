from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from app.db.session import get_db
from app.db.models import Model, ModelVersion

router = APIRouter(prefix="/models", tags=["models"])


class ModelCreate(BaseModel):
    name: str


class VersionCreate(BaseModel):
    version: str
    image_tag: str


@router.post("/")
def create_model(payload: ModelCreate, db: Session = Depends(get_db)):
    existing = db.query(Model).filter(Model.name == payload.name).first()
    if existing:
        raise HTTPException(status_code=409, detail="Model already exists")
    model = Model(name=payload.name)
    db.add(model)
    db.commit()
    db.refresh(model)
    return {"id": model.id, "name": model.name}


@router.get("/")
def list_models(db: Session = Depends(get_db)):
    models = db.query(Model).all()
    return [{"id": m.id, "name": m.name} for m in models]


@router.post("/{model_name}/versions")
def register_version(model_name: str, payload: VersionCreate, db: Session = Depends(get_db)):
    model = db.query(Model).filter(Model.name == model_name).first()
    if not model:
        raise HTTPException(status_code=404, detail="Model not found")

    version = ModelVersion(
        model_id=model.id,
        version=payload.version,
        image_tag=payload.image_tag,
    )
    db.add(version)
    db.commit()
    db.refresh(version)
    return {
        "id": version.id,
        "model": model.name,
        "version": version.version,
        "image_tag": version.image_tag,
    }


@router.get("/{model_name}/versions")
def list_versions(model_name: str, db: Session = Depends(get_db)):
    model = db.query(Model).filter(Model.name == model_name).first()
    if not model:
        raise HTTPException(status_code=404, detail="Model not found")

    return [
        {
            "id": v.id,
            "version": v.version,
            "image_tag": v.image_tag,
            "is_active": v.is_active,
        }
        for v in model.versions
    ]