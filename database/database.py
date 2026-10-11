
import sqlite3

from pathlib import Path

DB_PATH = Path(__file__).with_name("plant_monitor.db")


def initialize_database():
    connection = sqlite3.connect(DB_PATH)

    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS measurements (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            plant_id INTEGER NOT NULL,
            soil_moisture INTEGER NOT NULL,
            temperature REAL NOT NULL,
            humidity REAL NOT NULL,
            pressure REAL NOT NULL,
            light REAL NOT NULL
        )
    """)


    connection.commit()
    connection.close()


def save_measurement(
    timestamp,
    plant_id,
    soil_moisture,
    temperature,
    humidity,
    pressure,
    light,
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
            light
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (
            timestamp,
            plant_id,
            soil_moisture,
            temperature,
            humidity,
            pressure,
            light,
        ),
    )

    connection.commit()
    connection.close()



initialize_database()