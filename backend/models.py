from pydantic import BaseModel


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