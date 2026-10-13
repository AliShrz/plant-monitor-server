
from fastapi import FastAPI, HTTPException, Query

from database.database import get_latest_measurement, get_measurements

app = FastAPI(
    title="Plant Monitor API",
    description="API for retrieving plant monitoring data",
    version="1.0.0",
)


@app.get("/api/plants/{plant_id}/latest")
def get_latest_plant_measurement(plant_id: int):
    measurement = get_latest_measurement(plant_id)

    if measurement is None:
        raise HTTPException(
            status_code=404,
            detail=f"No measurements found for plant {plant_id}",
        )

    return measurement

@app.get("/api/plants/{plant_id}/measurements")
def get_plant_measurements(
    plant_id: int,
    limit: int = Query(default=20, ge=1, le=100)
):
    measurements = get_measurements(plant_id, limit)

    if not measurements:
        raise HTTPException(
            status_code=404,
            detail=f"No measurements found for plant {plant_id}",
        )

    return measurements