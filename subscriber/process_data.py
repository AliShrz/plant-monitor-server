from datetime import datetime

def process_data(data):

    date = data["data"]["date"]
    time = data["data"]["time"]

    timestamp = datetime.strptime(
        f"{date} {time}",
        "%d %b %Y %I:%M %p"
    ).strftime("%Y-%m-%d %H:%M:%S")

    plant_id = data["data"]["plant_id"]
    temperature = data["data"]["temperature"]
    humidity = data["data"]["humidity"]
    soil_moisture = data["data"]["soil_moisture"]
    pressure = data["data"]["pressure"]
    light = data["data"]["light"]
    wifi_ip = data["data"]["wifi_ip"]
    wifi_rssi = data["data"]["wifi_rssi"]

    print("Plant ID:", plant_id)
    print("Temperature:", temperature)
    print("Humidity:", humidity)
    print("Soil moisture:", soil_moisture)
    print("Pressure:", pressure)
    print("Light:", light)
    print("WiFi IP:", wifi_ip)
    print("WiFi RSSI:", wifi_rssi)

    return {
        "timestamp": timestamp,
        "plant_id": plant_id,
        "soil_moisture": soil_moisture,
        "temperature": temperature,
        "humidity": humidity,
        "pressure": pressure,
        "light": light,
        "wifi_ip": wifi_ip,
        "wifi_rssi": wifi_rssi,
    }
