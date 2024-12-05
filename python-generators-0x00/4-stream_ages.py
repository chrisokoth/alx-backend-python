import mysql.connector
from decouple import config

def connect_to_prodev():
    """Connect to the MySQL database."""
    return mysql.connector.connect(
        host="localhost",  
        user=config("DB_USER"),
        password=config("DB_PASSWORD"),  
        database="ALX_prodev"
    )

def stream_user_ages():
    """Generator function that yields user ages one by one."""
    connection = connect_to_prodev()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT age FROM user_data")  # Fetch only the age column
    for row in cursor:
        yield row['age']  # Yield each user's age
    connection.close()

def calculate_average_age():
    """Calculate the average age using the stream_user_ages generator."""
    total_age = 0
    count = 0
    for age in stream_user_ages():
        total_age += age
        count += 1
    if count == 0:
        return 0  # Avoid division by zero if no users are found
    return total_age / count

# Calculate and print the average age
average_age = calculate_average_age()
print(f"Average age of users: {average_age}")

