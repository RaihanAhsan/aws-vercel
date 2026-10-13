from app.database import db_cursor


def get_device_by_code(device_code: str):
    with db_cursor() as (_, cur):
        cur.execute(
            "SELECT id, device_code, device_name, api_key, is_active "
            "FROM devices WHERE device_code = %s",
            (device_code,)
        )
        return cur.fetchone()


def insert_reading(device_id: int, data: dict) -> int:
    with db_cursor() as (_, cur):
        cur.execute("""
            INSERT INTO sensor_readings
                (device_id, wind_speed, wind_direction, temperature,
                 humidity, pressure, solar_radiation, rainfall)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING id
        """, (
            device_id,
            data.get("wind_speed"),
            data.get("wind_direction"),
            data.get("temperature"),
            data.get("humidity"),
            data.get("pressure"),
            data.get("solar_radiation"),
            data.get("rainfall"),
        ))
        return cur.fetchone()["id"]


def get_latest(device_code: str):
    with db_cursor() as (_, cur):
        cur.execute("""
            SELECT r.*, d.device_code, d.device_name
            FROM sensor_readings r
            JOIN devices d ON d.id = r.device_id
            WHERE d.device_code = %s
            ORDER BY r.id DESC LIMIT 1
        """, (device_code,))
        return cur.fetchone()


def get_history(device_code: str, sensor: str, limit: int = 30):
    allowed = [
        "wind_speed", "wind_direction", "temperature",
        "humidity", "pressure", "solar_radiation", "rainfall"
    ]
    if sensor not in allowed:
        raise ValueError(f"Sensor '{sensor}' tidak valid")

    with db_cursor() as (_, cur):
        cur.execute(f"""
            SELECT r.{sensor} AS value, r.created_at
            FROM sensor_readings r
            JOIN devices d ON d.id = r.device_id
            WHERE d.device_code = %s
            ORDER BY r.id DESC LIMIT %s
        """, (device_code, limit))
        return list(reversed(cur.fetchall()))


def get_stats(device_code: str, sensor: str):
    allowed = [
        "wind_speed", "wind_direction", "temperature",
        "humidity", "pressure", "solar_radiation", "rainfall"
    ]
    if sensor not in allowed:
        raise ValueError(f"Sensor '{sensor}' tidak valid")

    with db_cursor() as (_, cur):
        cur.execute(f"""
            SELECT
                MIN(r.{sensor}) AS min,
                MAX(r.{sensor}) AS max,
                AVG(r.{sensor}) AS avg,
                COUNT(r.{sensor}) AS count
            FROM sensor_readings r
            JOIN devices d ON d.id = r.device_id
            WHERE d.device_code = %s
        """, (device_code,))
        row = cur.fetchone()
        if row:
            row["min"] = float(row["min"]) if row["min"] is not None else None
            row["max"] = float(row["max"]) if row["max"] is not None else None
            row["avg"] = float(row["avg"]) if row["avg"] is not None else None
        return row