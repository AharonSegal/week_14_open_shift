import os
import mysql.connector

def connect():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST", "mysql-service"),
        port=int(os.getenv("DB_PORT", "3306")),  
        user=os.getenv("DB_USER", "root"),
        password=os.getenv("DB_PASSWORD", "password"),
        database=os.getenv("DB_NAME", "weapons_db"),
    )

def init_db():
    # connect to db
    conn = connect()

    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS weapons (
            id INT AUTO_INCREMENT PRIMARY KEY,
            weapon_id VARCHAR(100),
            weapon_name VARCHAR(100),
            weapon_type VARCHAR(100),
            range_km INT,
            weight_kg FLOAT,
            manufacturer VARCHAR(100),
            origin_country VARCHAR(100),
            storage_location VARCHAR(100),
            year_estimated INT,
            level_risk VARCHAR(100)
        )
        """
    )
    conn.commit()
    cursor.close()
    conn.close()


def insert_weapons(dict_list):
    # insert dict_list to db
    connection = connect()
    cursor = connection.cursor()

    insert_sql = """
        INSERT INTO weapons (
            weapon_id,
            weapon_name,
            weapon_type,
            range_km,
            weight_kg,
            manufacturer,
            origin_country,
            storage_location,
            year_estimated,
            level_risk
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """

    values = []
    for item in dict_list:
        values.append(
            (
                item["weapon_id"],
                item["weapon_name"],
                item["weapon_type"],
                item["range_km"],
                item["weight_kg"],
                item["manufacturer"],
                item["origin_country"],
                item["storage_location"],
                item["year_estimated"],
                item["level_risk"],
            )
        )

    cursor.executemany(insert_sql, values)
    connection.commit()
    inserted_count = cursor.rowcount

    cursor.close()
    connection.close()

    return inserted_count
