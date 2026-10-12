# Smart Plant Monitoring System — Server

A modular Python-based server for the **Smart Plant Monitoring System**, designed to collect, process, and store sensor data transmitted by ESP32-based plant monitoring nodes.

The server runs on a NanoPi and uses MQTT for communication with ESP32 devices. Incoming sensor measurements are processed by a Python subscriber and stored in a local SQLite database for future analysis and visualization.

The project is designed with a modular architecture to support future backend APIs, a web dashboard, historical data visualization, and multi-plant monitoring.

---

# Current Status

**Project Stage**

MQTT Data Collection and Storage

**Overall Progress**

🟩🟩🟩🟩🟩⬜⬜⬜⬜⬜

### Completed

#### Project Setup
- Python server project initialized
- Git repository created
- Modular project structure established
- Local configuration and credentials excluded from Git
- Python virtual environment configured

#### MQTT Communication
- MQTT subscriber implemented using Paho MQTT
- Connection to the MQTT broker
- Subscription to configurable MQTT topics
- JSON payload parsing
- MQTT connection logging
- Automatic reconnection delay configuration

#### Data Processing
- Extraction of sensor measurements from JSON payloads
- Date and time conversion to a standardized timestamp format
- Processing of plant identification and sensor data
- Extraction of Wi-Fi connection information

#### Database
- SQLite database integration
- Automatic creation of the measurements table
- Parameterized SQL INSERT statements
- Storage of sensor measurements
- Storage of Wi-Fi IP address and signal strength
- Database initialization during application startup

### In Progress

- Backend API development
- Improving the server architecture
- Preparing data access for dashboard integration

### Planned

- REST API using FastAPI
- Latest sensor measurement endpoints
- Historical measurement endpoints
- Web dashboard
- Historical data visualization
- Multiple plant monitoring
- System and device status monitoring
- Automated service startup
- Deployment and operational documentation

---

# System Architecture

```text
                     ESP32 SENSOR NODE
                            |
                            | MQTT / JSON
                            v
                    +------------------+
                    |   MQTT Broker    |
                    |    Mosquitto     |
                    +--------+---------+
                             |
                             | MQTT Subscription
                             v
                    +------------------+
                    | MQTT Subscriber  |
                    |   subscriber/    |
                    +--------+---------+
                             |
                             | Parsed JSON
                             v
                    +------------------+
                    |  Data Processing |
                    |   process_data   |
                    +--------+---------+
                             |
                             | Processed Measurements
                             v
                    +------------------+
                    |  Database Layer  |
                    |    database/     |
                    +--------+---------+
                             |
                             v
                    +------------------+
                    |  SQLite Database |
                    | plant_monitor.db |
                    +------------------+

                   FUTURE COMPONENTS

                    +------------------+
                    |   FastAPI        |
                    |   Backend        |
                    +--------+---------+
                             |
                             v
                    +------------------+
                    |   Web Dashboard  |
                    +------------------+
```

---

# Project Structure

```text
plant-monitor/

├── backend/
│   └──                  # Future backend API
│
├── dashboard/
│   └──                  # Future web dashboard
│
├── database/
│   ├── __init__.py
│   ├── database.py
│   └── plant_monitor.db  # Generated locally
│
├── deployment/
│   └──                  # Future deployment configuration
│
├── docs/
│   └──                  # Project documentation
│
├── subscriber/
│   ├── __init__.py
│   ├── main.py
│   ├── process_data.py
│   ├── config.example.json
│   └── requirements.txt
│
├── .gitignore
└── README.md
```

The SQLite database and local configuration files are generated or maintained locally and are excluded from version control.

---

# Requirements

- NanoPi or another compatible Linux system
- Python 3.10 or newer
- An accessible MQTT broker
- Network connectivity between the ESP32 node and the MQTT broker

The subscriber currently uses **Paho MQTT 2.1.0**. SQLite is provided by Python's standard library and does not require a separate Python package.

---

# Getting Started

## 1. Clone the Repository

```bash
git clone git@github.com:AliShrz/plant-monitor-server.git
cd plant-monitor
```

If the repository has already been cloned, navigate to its local directory instead.

## 2. Create a Python Virtual Environment

```bash
python3 -m venv subscriber/.venv
```

## 3. Install Dependencies

```bash
subscriber/.venv/bin/python -m pip install -r subscriber/requirements.txt
```

## 4. Configure MQTT Credentials

Create a local configuration file from the example:

```bash
cp subscriber/config.example.json subscriber/config.json
```

Edit `subscriber/config.json` and provide the MQTT broker settings:

```json
{
    "broker": "YOUR_MQTT_BROKER_ADDRESS",
    "port": 1883,
    "username": "YOUR_MQTT_USERNAME",
    "password": "YOUR_MQTT_PASSWORD",
    "topic": "plant/1/state"
}
```

Replace the placeholder values with the actual broker address and credentials.

**Security:** Do not commit `subscriber/config.json` or expose MQTT credentials in source code. The local configuration file is excluded through `.gitignore`.

## 5. Run the Subscriber

Run the application from the project root:

```bash
subscriber/.venv/bin/python -m subscriber.main
```

The subscriber connects to the configured MQTT broker, subscribes to the specified topic, processes incoming JSON messages, and stores measurements in SQLite.

Example startup output:

```text
INFO: Connecting to MQTT broker
INFO: Connected to MQTT broker
INFO: Subscribed to topic: plant/1/state
```

The SQLite database is initialized automatically when the application starts.

---

# Database

The server currently uses SQLite for local data persistence.

The database file is located at:

```text
database/plant_monitor.db
```

## Measurements Table

The `measurements` table stores the following information:

| Column | Description |
|---|---|
| `id` | Unique measurement record ID |
| `timestamp` | Measurement date and time |
| `plant_id` | Plant identifier |
| `soil_moisture` | Soil moisture reading |
| `temperature` | Ambient temperature |
| `humidity` | Relative humidity |
| `pressure` | Atmospheric pressure |
| `light` | Ambient light intensity |
| `wifi_ip` | ESP32 Wi-Fi IP address |
| `wifi_rssi` | Wi-Fi received signal strength indicator |

Sensor measurements are stored as individual records, allowing historical data retrieval and analysis.

## Inspect Stored Measurements

Use Python to inspect the latest records:

```bash
subscriber/.venv/bin/python -c "import sqlite3; c=sqlite3.connect('database/plant_monitor.db'); print(*c.execute('SELECT * FROM measurements ORDER BY id DESC LIMIT 5').fetchall(), sep='\n'); c.close()"
```

---

# Development Roadmap

## Phase 1 — Project Foundation

- [x] Python project setup
- [x] GitHub repository
- [x] Modular directory structure
- [x] Virtual environment
- [x] MQTT configuration management

## Phase 2 — MQTT Data Collection

- [x] MQTT broker connectivity
- [x] MQTT topic subscription
- [x] JSON payload parsing
- [x] Sensor data extraction
- [x] Timestamp normalization
- [x] Wi-Fi information extraction

## Phase 3 — Data Persistence

- [x] SQLite integration
- [x] Measurements table
- [x] Database initialization
- [x] Parameterized database inserts
- [x] Sensor measurement storage
- [x] Wi-Fi IP and RSSI storage

## Phase 4 — Backend API

- [ ] FastAPI application
- [ ] Database query layer
- [ ] Latest measurement endpoint
- [ ] Historical measurement endpoint
- [ ] API documentation
- [ ] Backend testing

## Phase 5 — Web Dashboard

- [ ] Current sensor readings
- [ ] Historical sensor graphs
- [ ] Multiple plant monitoring
- [ ] Plant status overview
- [ ] Device connectivity indicators

## Phase 6 — Deployment and Automation

- [ ] Automatic subscriber startup
- [ ] Automatic backend startup
- [ ] Linux service configuration
- [ ] Service logs and operational monitoring
- [ ] Deployment documentation
- [ ] End-to-end testing

---

# Development Log

| Date | Description |
|---|---|
| 2026-10 | Initialized the server repository |
| 2026-10 | Configured the MQTT subscriber |
| 2026-10 | Implemented JSON data processing |
| 2026-10 | Added timestamp normalization |
| 2026-10 | Implemented SQLite database initialization |
| 2026-10 | Added measurement persistence |
| 2026-10 | Integrated Wi-Fi IP and RSSI storage |

---

# Future Architecture

The planned backend will expose a REST API for retrieving current and historical sensor measurements from the database.

The web dashboard will consume this API to display sensor readings, historical graphs, and plant monitoring information.

The MQTT subscriber, database layer, backend, and dashboard will remain separate components to improve maintainability and support future expansion.

---

# License

This project is currently under development. A license has not yet been specified.
