import os
import mysql.connector


def get_db_connection():
    connection = mysql.connector.connect(
        host=os.getenv("HOST"),
        user=os.getenv("USER"),
        password=os.getenv("PASSWORD"),
        database=os.getenv("DATABASE"),
        port=int(os.getenv("PORT", 3306))
    )

    return connection