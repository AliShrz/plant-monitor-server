# Plant Monitor Server

A modular Python-based server for collecting, processing, and storing sensor data from ESP32-based plant monitoring nodes.

The server runs on a NanoPi and uses MQTT for communication with ESP32 devices. Incoming sensor measurements are processed by a Python subscriber and stored in a local SQLite database.

The project is designed to support future backend APIs, a web dashboard, historical data visualization, and multi-plant monitoring.

---

## Current Status

**Project Stage:** MQTT Data Collection and Storage

### Implemented

- MQTT subscriber using Paho MQTT
- Connection to an MQTT broker
- Configurable MQTT topic subscription
- JSON payload parsing
- Sensor measurement extraction
- Timestamp normalization
- Wi-Fi IP and RSSI extraction
- SQLite database integration
- Automatic database initialization
- Measurement storage using parameterized SQL statements
- Local MQTT configuration file excluded from Git

### Planned

- REST API using FastAPI
- Latest measurement endpoint
- Historical measurement endpoints
- Web dashboard
- Historical sensor graphs
- Multiple plant monitoring
- Automated service startup
- Deployment documentation

---

## Architecture

```text
ESP32 Sensor Node
       |
       | MQTT / JSON
       v
   MQTT Broker
       |
       v
 MQTT Subscriber
       |
       v
 Data Processing
       |
       v
 Database Layer
       |
       v
 SQLite Database
       |
       v
 Future Backend API
       |
       v
 Future Web Dashboard
```

---

## Project Structure

```text
plant-monitor/
├── backend/
├── dashboard/
├── database/
│   ├── __init__.py
│   ├── database.py
│   └── plant_monitor.db
├── deployment/
├── docs/
├── subscriber/
│   ├── __init__.py
│   ├── main.py
│   ├── process_data.py
│   ├── config.example.json
│   └── requirements.txt
├── .gitignore
└── README.md
```

The SQLite database and local configuration files are excluded from version control.

---

## Requirements

- NanoPi or another compatible Linux system
- Python 3.10 or newer
- An accessible MQTT broker
- Network connectivity between the ESP32 node and the MQTT broker

The subscriber uses Paho MQTT 2.1.0. SQLite is provided by Python's standard library.

---

## Setup

### 1. Create a Virtual Environment

From the project root:

```bash
python3 -m venv subscriber/.venv
```

### 2. Install Dependencies

```bash
subscriber/.venv/bin/python -m pip install -r subscriber/requirements.txt
```

### 3. Configure MQTT

Create a local configuration file:

```bash
cp subscriber/config.example.json subscriber/config.json
```

Edit `subscriber/config.json` with your MQTT broker address, port, username, password, and topic.

Example configuration:

```json
{
    "broker": "YOUR_MQTT_BROKER_ADDRESS",
    "port": 1883,
    "username": "YOUR_MQTT_USERNAME",
    "password": "YOUR_MQTT_PASSWORD",
    "topic": "plant/1/state"
}
```

Do not commit `subscriber/config.json` or expose credentials in source code.

### 4. Run the Subscriber

Run the application from the project root:

```bash
subscriber/.venv/bin/python -m subscriber.main
```

The application connects to the MQTT broker, subscribes to the configured topic, processes incoming messages, and stores measurements in SQLite.

---

## Database

The database file is stored at:

```text
database/plant_monitor.db
```

The `measurements` table contains:

| Column | Description |
|---|---|
| `id` | Unique record identifier |
| `timestamp` | Measurement date and time |
| `plant_id` | Plant identifier |
| `soil_moisture` | Soil moisture reading |
| `temperature` | Ambient temperature |
| `humidity` | Relative humidity |
| `pressure` | Atmospheric pressure |
| `light` | Ambient light intensity |
| `wifi_ip` | ESP32 Wi-Fi IP address |
| `wifi_rssi` | Wi-Fi signal strength |

### Inspect Recent Measurements

```bash
subscriber/.venv/bin/python -c "import sqlite3; c=sqlite3.connect('database/plant_monitor.db'); print(*c.execute('SELECT * FROM measurements ORDER BY id DESC LIMIT 5').fetchall(), sep='\n'); c.close()"
```

---

## Development Roadmap

### Phase 1 — MQTT Data Collection

- [x] MQTT connection
- [x] Topic subscription
- [x] JSON payload parsing
- [x] Sensor data extraction

### Phase 2 — Data Persistence

- [x] SQLite integration
- [x] Database initialization
- [x] Measurement storage
- [x] Wi-Fi information storage

### Phase 3 — Backend API

- [ ] FastAPI application
- [ ] Latest measurement endpoint
- [ ] Historical measurement endpoint
- [ ] API testing

### Phase 4 — Dashboard

- [ ] Current sensor readings
- [ ] Historical graphs
- [ ] Multiple plant monitoring
- [ ] Plant status overview

### Phase 5 — Deployment

- [ ] Automatic service startup
- [ ] Backend service configuration
- [ ] Logging and operational monitoring
- [ ] Deployment documentation

---

## License

This project is currently under development. No license has been specified yet.
