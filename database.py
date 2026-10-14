import mysql.connector


def get_connection():
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="SAYALI12",
        database="ngo_management"
    )

    return connection