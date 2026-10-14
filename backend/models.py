from pydantic import BaseModel, Field


class MeasurementResponse(BaseModel):
    id: int
    timestamp: str
    plant_id: int
    soil_moisture: float
    temperature: float
    humidity: float
    pressure: float
    light: float
    wifi_ip: str
    wifi_rssi: int


class PlantCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)


class PlantUpdate(BaseModel):
    name: str = Field(min_length=1, max_length=100)


class PlantResponse(BaseModel):
    id: int
    name: str
    created_at: str