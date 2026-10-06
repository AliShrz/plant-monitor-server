import sqlite3

connection = sqlite3.connect("database/plant_monitor.db")
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

cursor.execute("PRAGMA table_info(measurements)")

print(cursor.fetchall())