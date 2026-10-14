
import sqlite3

from pathlib import Path
from datetime import datetime, timezone

DB_PATH = Path(__file__).with_name("plant_monitor.db")

def initialize_plants_table(connection):
    connection.execute("""
        CREATE TABLE IF NOT EXISTS plants (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
    """)

def initialize_devices_table(connection):
    connection.execute("""
        CREATE TABLE IF NOT EXISTS devices (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            plant_id INTEGER,
            created_at TEXT NOT NULL,
            FOREIGN KEY (plant_id) REFERENCES plants(id)
        )
    """)

def initialize_measurements_table(connection):
    connection.execute("""
        CREATE TABLE IF NOT EXISTS measurements (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            plant_id INTEGER NOT NULL,
            soil_moisture INTEGER NOT NULL,
            temperature REAL NOT NULL,
            humidity REAL NOT NULL,
            pressure REAL NOT NULL,
            light REAL NOT NULL,
            wifi_ip TEXT NOT NULL,
            wifi_rssi INTEGER NOT NULL
        )
    """)


def initialize_database():
    connection = sqlite3.connect(DB_PATH)

    cursor = connection.cursor()
    initialize_plants_table(connection)
    initialize_devices_table(connection)
    initialize_measurements_table(connection)

    connection.commit()
    connection.close()

def create_plant(name):
    name = name.strip()

    if not name:
        raise ValueError("Plant name cannot be empty")

    created_at = datetime.now(timezone.utc).isoformat()

    connection = sqlite3.connect(DB_PATH)

    try:
        cursor = connection.cursor()

        cursor.execute(
            """
            INSERT INTO plants (name, created_at)
            VALUES (?, ?)
            """,
            (name, created_at),
        )

        connection.commit()
        return cursor.lastrowid

    finally:
        connection.close()



def get_plants():
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row

    try:
        cursor = connection.cursor()

        cursor.execute("""
            SELECT id, name, created_at
            FROM plants
            ORDER BY id
        """)

        rows = cursor.fetchall()

        return [dict(row) for row in rows]

    finally:
        connection.close()

def get_plant_by_id(plant_id):
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row

    try:
        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT id, name, created_at
            FROM plants
            WHERE id = ?
            """,
            (plant_id,),
        )

        row = cursor.fetchone()

        if row is None:
            return None

        return dict(row)

    finally:
        connection.close()

def update_plant_name(plant_id, new_name):
    new_name = new_name.strip()

    if not new_name:
        raise ValueError("Plant name cannot be empty")

    connection = sqlite3.connect(DB_PATH)

    try:
        cursor = connection.cursor()

        cursor.execute(
            """
            UPDATE plants
            SET name = ?
            WHERE id = ?
            """,
            (new_name, plant_id),
        )

        connection.commit()

        return cursor.rowcount > 0

    finally:
        connection.close()

def delete_plant(plant_id):
    connection = sqlite3.connect(DB_PATH)

    try:
        cursor = connection.cursor()

        cursor.execute(
            """
            DELETE FROM plants
            WHERE id = ?
            """,
            (plant_id,),
        )

        connection.commit()

        return cursor.rowcount > 0

    finally:
        connection.close()

def save_measurement(
    timestamp,
    plant_id,
    soil_moisture,
    temperature,
    humidity,
    pressure,
    light,
    wifi_ip,
    wifi_rssi
):
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO measurements (
            timestamp,
            plant_id,
            soil_moisture,
            temperature,
            humidity,
            pressure,
            light,
            wifi_ip,
            wifi_rssi
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            timestamp,
            plant_id,
            soil_moisture,
            temperature,
            humidity,
            pressure,
            light,
            wifi_ip,
            wifi_rssi
        ),
    )

    connection.commit()
    connection.close()

def get_latest_measurement(plant_id):
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row

    try:
        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT *
            FROM measurements
            WHERE plant_id = ?
            ORDER BY timestamp DESC, id DESC
            LIMIT 1
            """,
            (plant_id,),
        )

        row = cursor.fetchone()

        if row is None:
            return None

        return dict(row)
        
    finally: 
        connection.close()


if __name__ == "__main__":
    initialize_database()

def get_measurements(plant_id, limit):
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row

    try:
        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT *
            FROM measurements
            WHERE plant_id = ?
            ORDER BY timestamp DESC, id DESC
            LIMIT ?
            """,
            (plant_id, limit),
        )

        rows = cursor.fetchall()

        return [dict(row) for row in rows]

    finally:
        connection.close()