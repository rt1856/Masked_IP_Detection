"""
FastAPI Microservice for Masked IP Detection
Real-time IP analysis with ML model integration
"""

from fastapi import FastAPI, HTTPException, BackgroundTasks, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field, validator
from typing import Optional, List, Dict, Any
import ipaddress
import joblib
import logging
from datetime import datetime
import numpy as np
from pathlib import Path
import redis
import json
import pandas as pd

# ============================================================================
# Path & App Setup
# ============================================================================

BASE_DIR = Path(__file__).resolve().parent.parent.parent
MODELS_DIR = BASE_DIR / "models"
DASHBOARD_DIR = BASE_DIR / "dashboard"

# Logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger("masked-ip-api")

# FastAPI app
app = FastAPI(
    title="Masked IP Detection API",
    description="ML-powered microservice for detecting masked/anonymous IP addresses",
    version="1.0.0",
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Static & Templates
app.mount(
    "/static",
    StaticFiles(directory=DASHBOARD_DIR / "static"),
    name="static",
)
templates = Jinja2Templates(directory=DASHBOARD_DIR / "templates")

# ============================================================================
# Globals
# ============================================================================

models: Dict[str, Any] = {}
feature_names: List[str] = []
ip_cache: Dict[str, Any] = {}

# Redis (optional)
try:
    redis_client = redis.Redis(host="localhost", port=6379, db=0, decode_responses=True)
    redis_client.ping()
    logger.info("Redis connected")
except Exception:
    redis_client = None
    logger.warning("Redis not available, using in-memory cache")

# ============================================================================
# Model Loading
# ============================================================================

def load_models():
    global models, feature_names

    try:
        models["random_forest"] = joblib.load(MODELS_DIR / "random_forest_model.pkl")
        models["xgboost"] = joblib.load(MODELS_DIR / "xgboost_model.pkl")
        feature_names.extend(joblib.load(MODELS_DIR / "feature_names.pkl"))

        logger.info(f"Loaded models: {list(models.keys())}")
        logger.info(f"Feature count: {len(feature_names)}")

    except Exception as e:
        logger.exception("Model loading failed")
        raise RuntimeError(str(e))


@app.on_event("startup")
async def startup():
    load_models()
    logger.info("Masked IP Detection API started")

# ============================================================================
# Pydantic Models
# ============================================================================

class IPCheckRequest(BaseModel):
    ip_address: str
    include_details: bool = True
    request_metadata: Optional[Dict[str, Any]] = None

    @validator("ip_address")
    def validate_ip(cls, v):
        ipaddress.ip_address(v)
        return v


class IPCheckResponse(BaseModel):
    ip_address: str
    is_masked: bool
    confidence: float
    risk_level: str
    detected_type: Optional[str]
    details: Optional[Dict[str, Any]]
    timestamp: str


class BatchIPCheckRequest(BaseModel):
    ip_addresses: List[str]
    include_details: bool = False


class HealthResponse(BaseModel):
    status: str
    models_loaded: int
    cache_available: bool
    timestamp: str

# ============================================================================
# Feature Engineering
# ============================================================================

def extract_ip_features(ip: str, metadata: Dict = None) -> Dict[str, Any]:
    ip_obj = ipaddress.ip_address(ip)
    features = {
        "ip_version": ip_obj.version,
        "is_private": int(ip_obj.is_private),
        "is_reserved": int(ip_obj.is_reserved),
        "is_loopback": int(ip_obj.is_loopback),
        "is_multicast": int(ip_obj.is_multicast),
        "latitude": 0.0,
        "longitude": 0.0,
        "accuracy_radius": 0,
        "asn": 0,
        "has_ptr_record": 0,
        "ptr_contains_host": 0,
        "in_tor_list": 0,
        "in_proxy_list": 0,
        "in_vpn_list": 0,
        "request_count": metadata.get("request_count", 1) if metadata else 1,
        "unique_user_agents": metadata.get("unique_user_agents", 1) if metadata else 1,
    }

    if ip_obj.version == 4:
        o = list(map(int, ip.split(".")))
        features.update(
            {"octet_1": o[0], "octet_2": o[1], "octet_3": o[2], "octet_4": o[3]}
        )
    else:
        features.update({f"octet_{i}": 0 for i in range(1, 5)})

    return features



def prepare_features(features: Dict[str, Any]) -> pd.DataFrame:
    return pd.DataFrame([[features.get(f, 0) for f in feature_names]],
                         columns=feature_names)

# ============================================================================
# Prediction
# ============================================================================

def predict_masked_ip(ip: str, metadata: Dict = None) -> Dict[str, Any]:
    cache_key = f"ip:{ip}"

    if redis_client:
        cached = redis_client.get(cache_key)
        if cached:
            return json.loads(cached)
    elif ip in ip_cache:
        return ip_cache[ip]

    features = extract_ip_features(ip, metadata)
    X = prepare_features(features)

    probabilities = {}
    for name, model in models.items():
        prob = model.predict_proba(X)[0]
        probabilities[name] = float(prob[1])


    ensemble_prob = sum(probabilities.values()) / len(probabilities)
    is_masked = ensemble_prob > 0.5
    confidence = ensemble_prob if is_masked else 1 - ensemble_prob

    risk = (
        "CRITICAL" if confidence > 0.9 else
        "HIGH" if confidence > 0.7 else
        "MEDIUM" if confidence > 0.5 else "LOW"
    )

    result = {
    "is_masked": bool(is_masked),
    "confidence": float(confidence),
    "risk_level": str(risk),
    "detected_type": str("masked") if is_masked else None,
    "ensemble_probability": float(ensemble_prob),
    "features": {k: float(v) if isinstance(v, (np.integer, np.floating)) else int(v) if isinstance(v, np.bool_) else v
                 for k, v in features.items()},
    }


    if redis_client:
        redis_client.setex(cache_key, 3600, json.dumps(result))
    else:
        ip_cache[ip] = result

    return result

# ============================================================================
# ROUTES
# ============================================================================

@app.get("/", response_class=HTMLResponse)
async def ui(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/api")
async def api_info():
    return {
        "service": "Masked IP Detection API",
        "version": "1.0.0",
        "status": "operational",
        "endpoints": {
            "health": "/health",
            "check": "/api/v1/check",
            "batch": "/api/v1/batch",
            "stats": "/api/v1/stats",
        },
    }


@app.get("/health", response_model=HealthResponse)
async def health():
    return HealthResponse(
        status="healthy",
        models_loaded=len(models),
        cache_available=redis_client is not None,
        timestamp=datetime.now().isoformat(),
    )


@app.post("/api/v1/check", response_model=IPCheckResponse)
async def check_ip(req: IPCheckRequest):
    result = predict_masked_ip(req.ip_address, req.request_metadata)
    return IPCheckResponse(
        ip_address=req.ip_address,
        is_masked=result["is_masked"],
        confidence=result["confidence"],
        risk_level=result["risk_level"],
        detected_type=result["detected_type"],
        details=result if req.include_details else None,
        timestamp=datetime.now().isoformat(),
    )


@app.post("/api/v1/batch")
async def batch_check(req: BatchIPCheckRequest):
    results = []
    for ip in req.ip_addresses:
        try:
            ipaddress.ip_address(ip)
            r = predict_masked_ip(ip)
            results.append({"ip": ip, **r})
        except Exception as e:
            results.append({"ip": ip, "error": str(e)})

    return {"total": len(req.ip_addresses), "results": results}


@app.get("/api/v1/stats")
async def stats():
    return {
        "models_loaded": len(models),
        "feature_count": len(feature_names),
        "cache_size": len(ip_cache),
        "cache_type": "redis" if redis_client else "memory",
        "timestamp": datetime.now().isoformat(),
    }
