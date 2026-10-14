# Smart Plant Monitoring System — Server

A modular Python-based server for the **Smart Plant Monitoring System**, designed to collect, process, store, and serve sensor data from ESP32-based plant monitoring devices.

The server runs on a NanoPi or another compatible Linux system. It uses MQTT for communication with ESP32 devices, SQLite for local data persistence, and FastAPI to expose sensor measurements through a REST API.

The long-term goal is to provide a complete plant monitoring product that users can operate through a web dashboard without directly accessing the server, editing database records, or writing code.

The planned dashboard will support plant management, device configuration, current sensor readings, and historical data visualization.

---

# Current Status

**Project Stage:** MQTT Data Collection, Storage, and Initial Backend API

**Overall Progress:** Core data collection and persistence are implemented. Backend API development is in progress.

### Completed

#### Project Setup
- Python server project initialized
- Git repository established
- Modular project structure created
- Local configuration and credentials excluded from version control
- Python virtual environment configured

#### MQTT Communication
- MQTT subscriber implemented using Paho MQTT
- Connection to the MQTT broker
- Subscription to configured MQTT topics
- JSON payload parsing
- MQTT connection logging
- Automatic reconnection delay configuration

#### Data Processing
- Extraction of sensor measurements from JSON payloads
- Timestamp normalization
- Processing of plant identification and sensor measurements
- Extraction of ESP32 Wi-Fi connection information

#### Database
- SQLite integration
- Automatic initialization of the measurements table
- Parameterized SQL INSERT statements
- Storage of sensor measurements
- Storage of Wi-Fi IP address and signal strength
- Database query functions for retrieving measurements

#### Backend API
- FastAPI application implemented in `backend/main.py`
- Endpoint for retrieving the latest plant measurement
- Endpoint for retrieving historical measurements
- Query parameter validation for history limits
- Pydantic response model implemented in `backend/models.py`
- Automatic interactive API documentation
- Basic endpoint testing completed

### In Progress

- Refining the backend architecture
- Designing the plant and device data models
- Planning database relationships and data migration
- Preparing API endpoints for dashboard integration

### Planned

- Automatic creation of database tables
- Plant registration and management through the API
- Device registration and plant assignment
- Plant and device configuration through the dashboard
- Validation of plant and device identifiers
- Current sensor readings and historical graphs
- Device connectivity and system status monitoring
- Automated service startup
- Deployment, backup, and operational documentation

---

# System Architecture

```text
                     ESP32 SENSOR NODES
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
                             | Data Processing
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
                    +--------+---------+
                             |
                             | Database Queries
                             v
                    +------------------+
                    |     FastAPI      |
                    |    backend/      |
                    +--------+---------+
                             |
                             | REST API / JSON
                             v
                    +------------------+
                    |  Web Dashboard   |
                    |    dashboard/    |
                    +------------------+

                 PLANNED MANAGEMENT FEATURES

                 - Plant registration and editing
                 - Device registration and assignment
                 - Plant and device settings
                 - Historical sensor graphs
                 - Device status monitoring
```

The components have separate responsibilities:

- **ESP32 devices:** Collect sensor readings and publish measurements.
- **MQTT broker:** Receives and distributes messages from connected devices.
- **MQTT subscriber:** Processes incoming messages and stores measurements.
- **Database layer:** Provides database initialization and data access functions.
- **SQLite:** Stores sensor measurements and will store plant and device metadata.
- **FastAPI:** Exposes data and management operations through HTTP endpoints.
- **Web dashboard:** Provides the user interface for monitoring and managing the system.

The dashboard will communicate with the backend through the REST API. It will not access the SQLite database directly.

---

# Project Structure

```text
plant-monitor/

├── .venv/ 
├── backend/
│   ├── __init__.py
│   ├── main.py
│   └── models.py
│
├── dashboard/
│   └──                  # Web dashboard (planned)
│
├── database/
│   ├── __init__.py
│   ├── database.py
│   └── plant_monitor.db  # Generated locally
│
├── deployment/
│   └──                  # Deployment configuration (planned)
│
├── docs/
│   └──                  # Project documentation
│
├── subscriber/
│   ├── __init__.py
│   ├── main.py
│   ├── process_data.py
│   └── config.example.json
│
├── requirements.txt
├── .gitignore
└── README.md
```

The SQLite database and local configuration files are maintained locally and excluded from version control.

---

# Requirements

- NanoPi or another compatible Linux system
- Python 3.10 or newer
- An accessible MQTT broker
- Network connectivity between ESP32 devices and the MQTT broker
- Git for version control

The subscriber uses Paho MQTT 2.1.0. SQLite is provided by Python's standard library.

The backend uses FastAPI and Uvicorn. The subscriber and backend share the project's Python environment during development.

---

# Getting Started

## 1. Clone the Repository

```bash
git clone git@github.com:AliShrz/plant-monitor-server.git
cd plant-monitor
```

If the repository has already been cloned, navigate to the existing project directory.

## 2. Create a Python Virtual Environment

```bash
python3 -m venv subscriber/.venv
```

## 3. Install Subscriber Dependencies

```bash
subscriber/.venv/bin/python -m pip install -r subscriber/requirements.txt
```

## 4. Install Backend Dependencies

```bash
subscriber/.venv/bin/python -m pip install fastapi uvicorn
```

## 5. Configure MQTT Credentials

Create a local configuration file from the example:

```bash
cp subscriber/config.example.json subscriber/config.json
```

Edit `subscriber/config.json` with the MQTT broker address and credentials:

```json
{
    "broker": "YOUR_MQTT_BROKER_ADDRESS",
    "port": 1883,
    "username": "YOUR_MQTT_USERNAME",
    "password": "YOUR_MQTT_PASSWORD",
    "topic": "plant/1/state"
}
```

Replace the placeholder values with the actual broker settings.

**Security:** Never commit `subscriber/config.json` or expose MQTT credentials in source code. The local configuration file is excluded through `.gitignore`.

---

# Running the Server Components

## 1. Start the MQTT Subscriber

Run from the project root:

```bash
subscriber/.venv/bin/python -m subscriber.main
```

The subscriber connects to the configured MQTT broker, subscribes to the configured topic, processes incoming JSON messages, and stores measurements in SQLite.

Example startup output:

```text
INFO: Connecting to MQTT broker
INFO: Connected to MQTT broker
INFO: Subscribed to topic: plant/1/state
```

The database is initialized automatically by the existing database initialization code.

## 2. Start the FastAPI Backend

Open another terminal from the project root and run:

```bash
subscriber/.venv/bin/python -m uvicorn backend.main:app --host 0.0.0.0 --port 8000
```

The backend exposes the REST API on port `8000`.

For local development, open:

- Interactive API documentation: `http://127.0.0.1:8000/docs`
- Alternative API documentation: `http://127.0.0.1:8000/redoc`

To access the API from another device on the same network, replace `127.0.0.1` with the server's LAN IP address.

The `0.0.0.0` bind address allows network interfaces to accept connections. Use appropriate firewall rules and authentication before exposing the service to untrusted networks.

---

# REST API

The backend currently provides read-only endpoints for retrieving plant measurements.

## Available Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/api/plants/{plant_id}/latest` | Retrieve the latest measurement for a plant |
| `GET` | `/api/plants/{plant_id}/measurements` | Retrieve historical measurements for a plant |

### Latest Measurement

Example request:

```http
GET /api/plants/1/latest
```

Returns the latest stored measurement for the requested plant.

### Historical Measurements

Example request:

```http
GET /api/plants/1/measurements?limit=20
```

The `limit` query parameter controls the maximum number of returned records. Its default value is `20`, and the accepted range is `1` to `100`.

### Response Models

The backend defines a Pydantic response model in `backend/models.py`.

The model specifies the expected fields and data types for a measurement response. FastAPI uses the model for response validation and API documentation.

### Current Error Handling

- `404 Not Found`: The current endpoints return this response when no measurements are found for the requested plant.
- `422 Unprocessable Entity`: Invalid path or query parameter values, such as an out-of-range history limit, are rejected by FastAPI validation.

**Planned improvement:** After introducing a dedicated `plants` table, the API will distinguish between a nonexistent plant and an existing plant without measurements. A nonexistent plant will return `404`; an existing plant with no historical measurements will return `200 OK` with an empty list (`[]`).

---

# Database

The server currently uses SQLite for local data persistence.

Database file:

```text
database/plant_monitor.db
```

## Current Measurements Table

The `measurements` table stores sensor readings and device network information.

| Column | Description |
|---|---|
| `id` | Unique measurement record ID |
| `timestamp` | Measurement date and time |
| `plant_id` | Plant identifier associated with the measurement |
| `soil_moisture` | Soil moisture reading |
| `temperature` | Ambient temperature |
| `humidity` | Relative humidity |
| `pressure` | Atmospheric pressure |
| `light` | Ambient light intensity |
| `wifi_ip` | ESP32 Wi-Fi IP address |
| `wifi_rssi` | Wi-Fi received signal strength indicator |

Each measurement is stored as an individual record, enabling historical data retrieval and analysis.

The current database contains the `measurements` table. A dedicated `plants` table and device registry have not yet been implemented.

## Planned Database Design

The database will be extended to support product-level management.

### `plants`

Stores registered plants and their metadata, such as:

- Unique plant ID
- Plant name
- Creation timestamp
- Active or inactive status

### `devices`

Stores registered ESP32 devices and their metadata, such as:

- Unique device ID
- Device configuration
- Assignment to a plant
- Active or inactive status

### `measurements`

Continues to store historical sensor measurements, with relationships to the registered plants and, where appropriate, the reporting devices.

The plant ID and device ID will be separate identifiers. This allows device assignments to change without changing the identity of a plant or losing its historical measurements.

**Migration requirement:** Existing measurement records must be preserved when the new tables and relationships are introduced. Existing plant identifiers will need to be reconciled with the new plant registry.

Database schema creation and initialization will be handled by application code. Users will not need to create tables manually.

## Inspect Stored Measurements

To inspect the latest five records:

```bash
subscriber/.venv/bin/python -c "import sqlite3; c=sqlite3.connect('database/plant_monitor.db'); print(*c.execute('SELECT * FROM measurements ORDER BY id DESC LIMIT 5').fetchall(), sep='\n'); c.close()"
```

This command is intended for development and troubleshooting, not normal dashboard operation.

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
- [x] Latest and historical measurement query functions

## Phase 4 — Backend API

- [x] FastAPI application
- [x] Latest measurement endpoint
- [x] Historical measurement endpoint
- [x] Pydantic response model
- [x] Automatic API documentation
- [x] Basic endpoint testing
- [ ] Dedicated API tests
- [ ] Plant existence validation
- [ ] Standardized empty-history behavior
- [ ] Plant management endpoints
- [ ] Device management endpoints

## Phase 5 — Database and Device Management

- [ ] Design the `plants` and `devices` tables
- [ ] Implement automatic schema creation
- [ ] Preserve and migrate existing measurement data
- [ ] Define relationships between plants, devices, and measurements
- [ ] Validate incoming plant and device identifiers
- [ ] Support plant registration, editing, and deactivation
- [ ] Support device registration and plant assignment

## Phase 6 — Web Dashboard

- [ ] Current sensor readings
- [ ] Historical sensor graphs
- [ ] Plant list and plant details
- [ ] Add and rename plants
- [ ] Device assignment and configuration
- [ ] Device connectivity indicators
- [ ] Plant status overview
- [ ] API integration
- [ ] User-friendly error handling

## Phase 7 — Deployment and Automation

- [ ] Automatic subscriber startup
- [ ] Automatic backend startup
- [ ] Linux service configuration
- [ ] Service logs and operational monitoring
- [ ] Database backup and recovery
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
| 2026-10 | Added Wi-Fi IP and RSSI storage |
| 2026-10 | Implemented latest measurement API |
| 2026-10 | Implemented historical measurement API |
| 2026-10 | Added Pydantic response models and tested API endpoints |

---

# Future Architecture and Product Goals

The long-term objective is to provide a complete plant monitoring product that can be managed through a user-friendly dashboard.

Users should be able to perform routine operations without accessing the NanoPi or interacting directly with the database.

Planned capabilities include:

- Registering plants and changing their names
- Registering ESP32 devices and assigning them to plants
- Viewing current sensor readings
- Exploring historical measurements through graphs
- Monitoring device connectivity and system status
- Managing settings through the dashboard

The backend will expose the necessary REST API endpoints. The database layer will manage persistence and relationships, while the MQTT subscriber will continue to process incoming sensor data.

Database tables will be created automatically during application initialization. Existing data will be preserved when the schema is extended.

The architecture will keep the subscriber, database layer, backend API, and dashboard as separate components to improve maintainability and support future expansion.

---

# License

This project is currently under development. A license has not yet been specified.
