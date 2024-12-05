from decouple import config
import mysql.connector

def connect_db():
    """Connect to the MySQL database."""
    return mysql.connector.connect(
        host="localhost",  
        user=config("DB_USER"),
        password=config("DB_PASSWORD")  
        database="ALX_prodev"
    )

def stream_users():
    """Generator function to stream users one by one."""
    connection = connect_db()
    cursor = connection.cursor(dictionary=True)  
    cursor.execute("SELECT user_id, name, email, age FROM user_data")

    # Yield each row one by one
    for row in cursor:
        yield row

    cursor.close()
    connection.close()
