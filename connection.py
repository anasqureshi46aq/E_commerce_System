import mysql.connector


def create_connection():
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="2829",
        database="e_commerce_db"
    )

    return connection