

def process_data(data):
    plant_id = data["data"]["plant_id"]
    temperature = data["data"]["temperature"]
    humidity = data["data"]["humidity"]
    soil_moisture = data["data"]["soil_moisture"]
    pressure = data["data"]["pressure"]
    light = data["data"]["light"]
    wifi_rssi = data["data"]["wifi_rssi"]
    wifi_ip = data["data"]["wifi_ip"]

    print("Plant ID:", plant_id)
    print("Temperature:", temperature)
    print("Humidity:", humidity)
    print("Soil moisture:", soil_moisture)
    print("Pressure:", pressure)
    print("Light:", light)
    print("WiFi RSSI:", wifi_rssi)
    print("WiFi IP:", wifi_ip)