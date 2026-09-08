from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, field_validator
from app.k8s.client import scale_deployment

router = APIRouter(prefix="/deployments", tags=["deployments"])

V1_DEPLOYMENT_NAME = "model-service"
V2_DEPLOYMENT_NAME = "model-service-v2"


class CanaryRequest(BaseModel):
    total_replicas: int = 3
    v1_weight: int
    v2_weight: int

    @field_validator("v2_weight")
    @classmethod
    def weights_must_sum_to_100(cls, v2_weight, info):
        v1_weight = info.data.get("v1_weight")
        if v1_weight is not None and v1_weight + v2_weight != 100:
            raise ValueError("v1_weight and v2_weight must sum to 100")
        return v2_weight


@router.post("/canary")
def set_canary_split(payload: CanaryRequest):
    v1_replicas = round(payload.total_replicas * payload.v1_weight / 100)
    v2_replicas = payload.total_replicas - v1_replicas

    if payload.v1_weight > 0:
        v1_replicas = max(v1_replicas, 1)
    if payload.v2_weight > 0:
        v2_replicas = max(v2_replicas, 1)

    try:
        v1_result = scale_deployment(V1_DEPLOYMENT_NAME, v1_replicas)
        v2_result = scale_deployment(V2_DEPLOYMENT_NAME, v2_replicas)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Kubernetes scaling failed: {e}")

    return {
        "v1": v1_result,
        "v2": v2_result,
        "approx_split": f"{payload.v1_weight}% v1 / {payload.v2_weight}% v2",
    }