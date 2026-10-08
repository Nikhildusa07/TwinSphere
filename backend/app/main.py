import os
from datetime import datetime, timedelta, timezone

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.action_feedback import router as action_feedback_router
from app.api.dashboard import router as dashboard_router
from app.api.digital_twin import router as digital_twin_router
from app.api.prediction import router as prediction_router
from app.api.sensor_data import router as sensor_data_router
from app.db.database import Base, SessionLocal, engine
from app.models.action_feedback import ActionFeedback
from app.models.digital_twin import DigitalTwin
from app.models.sensor_data import SensorData


Base.metadata.create_all(bind=engine)


def seed_initial_data():
    db = SessionLocal()

    try:
        existing_twin = (
            db.query(DigitalTwin)
            .order_by(DigitalTwin.id.asc())
            .first()
        )

        if existing_twin is not None:
            return

        twin = DigitalTwin(
            name="Factory Machine 01",
            entity_type="Industrial Machine",
            temperature=82.3,
            vibration=3.9,
            power_usage=18.7,
            operating_speed=1520,
            status="normal",
        )

        db.add(twin)
        db.flush()

        sensor_readings = [
            (78.4, 3.1, 17.2, 1480),
            (79.1, 3.2, 17.5, 1490),
            (79.8, 3.4, 17.8, 1500),
            (80.2, 3.5, 18.0, 1505),
            (80.9, 3.6, 18.2, 1510),
            (81.3, 3.7, 18.4, 1515),
            (81.7, 3.8, 18.5, 1518),
            (82.0, 3.8, 18.6, 1520),
            (82.2, 3.9, 18.7, 1520),
            (82.3, 3.9, 18.7, 1520),
        ]

        current_time = datetime.now(timezone.utc)

        for index, (
            temperature,
            vibration,
            power_usage,
            operating_speed,
        ) in enumerate(sensor_readings):

            reading = SensorData(
                digital_twin_id=twin.id,
                temperature=temperature,
                vibration=vibration,
                power_usage=power_usage,
                operating_speed=operating_speed,
                recorded_at=current_time
                - timedelta(minutes=(len(sensor_readings) - index) * 5),
            )

            db.add(reading)

        db.commit()

    except Exception:
        db.rollback()
        raise

    finally:
        db.close()


seed_initial_data()


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