
from fastapi import FastAPI, HTTPException, Query
from datetime import datetime, timezone

from database.database import (
    create_plant,
    get_plants,
    get_plant_by_id,
    update_plant_name,
    delete_plant,
    reset_plant
)
from backend.models import (
    MeasurementResponse,
    PlantCreate,
    PlantUpdate,
    PlantResponse,
)


app = FastAPI(
    title="Plant Monitor API",
    description="API for retrieving plant monitoring data",
    version="1.0.0",
)


@app.get(
    "/api/plants/{plant_id}/latest",
    response_model=MeasurementResponse
)
def get_latest_plant_measurement(plant_id: int):
    measurement = get_latest_measurement(plant_id)

    if measurement is None:
        raise HTTPException(
            status_code=404,
            detail=f"No measurements found for plant {plant_id}",
        )

    return measurement

@app.get(
    "/api/plants/{plant_id}/measurements",
    response_model=list[MeasurementResponse]
)
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

@app.post("/api/plants", response_model=PlantResponse, status_code=201)
def create_new_plant(plant: PlantCreate):
    try:
        plant_id = create_plant(plant.name)
        return get_plant_by_id(plant_id)

    except ValueError as error:
        raise HTTPException(status_code=422, detail=str(error))

@app.get("/api/plants", response_model=list[PlantResponse])
def read_plants():
    return get_plants()

@app.get("/api/plants/{plant_id}", response_model=PlantResponse)
def read_plant(plant_id: int):
    plant = get_plant_by_id(plant_id)

    if plant is None:
        raise HTTPException(
            status_code=404,
            detail=f"Plant {plant_id} not found",
        )

    return plant

@app.patch("/api/plants/{plant_id}", response_model=PlantResponse)
def rename_plant(plant_id: int, plant: PlantUpdate):
    updated = update_plant_name(plant_id, plant.name)

    if not updated:
        raise HTTPException(
            status_code=404,
            detail=f"Plant {plant_id} not found",
        )

    return get_plant_by_id(plant_id)

@app.post("/api/plants/{plant_id}/reset", status_code=204)
def reset_plant_data(plant_id: int):
    plant = get_plant_by_id(plant_id)

    if plant is None:
        raise HTTPException(
            status_code=404,
            detail=f"Plant {plant_id} not found",
        )

    reset_plant(plant_id)
    return None

@app.delete("/api/plants/{plant_id}", status_code=204)
def remove_plant(plant_id: int):
    deleted = delete_plant(plant_id)

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail=f"Plant {plant_id} not found",
        )

    return None