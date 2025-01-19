from decouple import config
from configparser import Error
import mysql.connector
import csv
import uuid
import os

# Database connection function
def connect_db():
    """Connect to the MySQL database server."""
    try:
        # Attempting to connect to MySQL server
        connection = mysql.connector.connect(
            host="localhost",  
            user=config("DB_USER"),
            password=config("DB_PASSWORD")
        )
        if connection.is_connected():  # Check if connection is successful
            print("Database connected successfully")
        return connection
    except Error as e:
        print(f"Error: {e}")
        return None
    

# Create database if it doesn't exist
def create_database(connection):
    """Create the database ALX_prodev if it does not exist."""
    cursor = connection.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS ALX_prodev")
    connection.commit()
    cursor.close()

# Connect to the ALX_prodev database
def connect_to_prodev():
    """Connect to the ALX_prodev database."""
    connection = connect_db()
    connection.database = "ALX_prodev"
    return connection


# Create the user_data table if it doesn't exist
def create_table(connection):
    """Create the user_data table if it does not exist."""
    cursor = connection.cursor()
    create_table_query = """
    CREATE TABLE IF NOT EXISTS user_data (
        user_id CHAR(36) PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        email VARCHAR(255) NOT NULL,
        age DECIMAL(10, 2) NOT NULL
    );
    """
    cursor.execute(create_table_query)
    connection.commit()
    cursor.close()

# Insert data into the user_data table
def insert_data(connection, data):
    """Insert data into the user_data table if it does not exist."""
    cursor = connection.cursor()
    insert_query = """
    INSERT INTO user_data (user_id, name, email, age)
    VALUES (%s, %s, %s, %s)
    """
    # Insert data (make sure to avoid duplicates based on user_id)
    for row in data:
        cursor.execute(insert_query, row)
    connection.commit()
    cursor.close()

# Load data from the CSV file and prepare it for insertion
import csv
import uuid
import os

def load_data_from_csv(file_name="user_data.csv"):
    """Load data from the CSV file."""
    data = []
    # Get the absolute path to the CSV file based on the current working directory
    file_path = os.path.join(os.getcwd(), file_name)

    try:
        with open(file_path, newline='', encoding='utf-8') as csvfile:
            csvreader = csv.reader(csvfile)
            next(csvreader)  # Skip the header row
            
            for row in csvreader:
                print(f"Raw row: {row}")  # Print raw row for debugging

                # Check if the row is empty or does not have enough columns
                if not row or len(row) < 3:  
                    print(f"Skipping empty or malformed row: {row}")
                    continue
                
                # Ensure the row has 3 valid columns
                name = row[0].strip() if len(row) > 0 else ''
                email = row[1].strip() if len(row) > 1 else ''
                age = row[2].strip() if len(row) > 2 else ''
                
                # Skip rows that have any missing or empty values
                if not name or not email or not age:
                    print(f"Skipping incomplete row: {row}")
                    continue

                try:
                    age = float(age)  # Convert age to a float (may throw ValueError if not a number)
                except ValueError:
                    print(f"Skipping row with invalid age value: {row}")
                    continue

                user_id = str(uuid.uuid4())  # Generate unique UUID for each user
                data.append((user_id, name, email, age))

        print(f"Data loaded successfully from {file_path}")
    except Exception as e:
        print(f"Error loading CSV file: {e}")
    
    return data




# Load data from the CSV file and prepare it for insertion
def load_data_from_csv(file_name="user_data.csv"):
    """Load data from the CSV file."""
    data = []
    # Get the absolute path to the CSV file based on the current working directory
    file_path = os.path.join(os.getcwd(), file_name)

    try:
        with open(file_path, newline='') as csvfile:
            csvreader = csv.reader(csvfile)
            next(csvreader)  # Skip header row
            for row in csvreader:
                user_id = str(uuid.uuid4())  # Generate unique UUID for each user
                name = row[0]
                email = row[1]
                age = row[2]
                data.append((user_id, name, email, age))  # Append user data to the list
        print(f"Data loaded successfully from {file_path}")
    except Exception as e:
        print(f"Error loading CSV file: {e}")
    
    return data


# Generator function to stream rows from the database
def stream_rows_from_db():
    """Stream rows from the user_data table one by one."""
    connection = connect_to_prodev()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM user_data")
    for row in cursor:
        yield row  # Yield each row one by one
    cursor.close()
    connection.close()


# Main function to set up database, table, and insert data
def main():
    """Set up the database, table, and insert data from the CSV."""
    try:
        connection = connect_db()
        create_database(connection)  # Create database if not exists
        connection.close()  # Close initial connection to the MySQL server
        
        # Connect to the ALX_prodev database and create table
        connection = connect_to_prodev()
        create_table(connection)  # Create the user_data table if not exists
        
        # Load data from CSV file and insert it into the database
        file_path = "user_data.csv"  # Specify your CSV file path
        data = load_data_from_csv(file_path)
        insert_data(connection, data)  # Insert data into the user_data table
        connection.close()  # Close the database connection

        # Streaming data from the database
        print("Streaming data from the database:")
        for row in stream_rows_from_db():
            print(row)

    except mysql.connector.Error as err:
        print(f"Error: {err}")
    except Exception as e:
        print(f"Unexpected error: {e}")

# Run the script
if __name__ == "__main__":
    main()