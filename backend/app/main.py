import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.action_feedback import router as action_feedback_router
from app.api.dashboard import router as dashboard_router
from app.api.digital_twin import router as digital_twin_router
from app.api.prediction import router as prediction_router
from app.api.sensor_data import router as sensor_data_router
from app.db.database import Base, engine
from app.models.action_feedback import ActionFeedback
from app.models.digital_twin import DigitalTwin
from app.models.sensor_data import SensorData


Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="TwinSphere",
    description="Autonomous Digital Twin & Predictive Decision Intelligence",
    version="1.0.0",
)


frontend_urls = os.getenv(
    "FRONTEND_URLS",
    "http://localhost:5173,http://127.0.0.1:5173",
)

allow_origins = [
    url.strip()
    for url in frontend_urls.split(",")
    if url.strip()
]


app.add_middleware(
    CORSMiddleware,
    allow_origins=allow_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(digital_twin_router)
app.include_router(sensor_data_router)
app.include_router(prediction_router)
app.include_router(action_feedback_router)
app.include_router(dashboard_router)


@app.get("/")
def root():
    return {
        "project": "TwinSphere",
        "status": "running",
        "message": "TwinSphere API is online",
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
    }