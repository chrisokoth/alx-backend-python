import mysql.connector
import csv
import os
import uuid
from decouple import config

# Database connection function
def connect_db():
    """Connect to the MySQL database server."""
    try:
        connection = mysql.connector.connect(
            host="localhost",  
            user=config("DB_USER"),
            password=config("DB_PASSWORD")
        )
        if connection.is_connected():
            print("Database connected successfully")
        return connection
    except mysql.connector.Error as err:
        print(f"Error: {err}")
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
    """Insert data into the user_data table."""
    cursor = connection.cursor()
    insert_query = """
    INSERT INTO user_data (user_id, name, email, age)
    VALUES (%s, %s, %s, %s)
    """
    for row in data:
        cursor.execute(insert_query, row)
    connection.commit()
    cursor.close()

# Load data from the CSV file and prepare it for insertion
# Load data from the CSV file and prepare it for insertion
def load_data_from_csv(file_name="user_data.csv"):
    """Load data from the CSV file."""
    data = []
    file_path = os.path.join(os.getcwd(), file_name)

    try:
        with open(file_path, newline='', encoding='utf-8') as csvfile:
            csvreader = csv.reader(csvfile, quotechar='"')  # Handle quotes properly
            next(csvreader)  # Skip the header row
            row_counter = 0  # Track number of rows read
            for row in csvreader:
                row_counter += 1
                if not row or len(row) < 3:
                    print(f"Skipping invalid row {row_counter}: {row}")
                    continue

                # Ensure there are exactly 3 values in the row
                name = row[0].strip()
                email = row[1].strip()
                age = row[2].strip()

                # Validate that age is a number
                try:
                    age = float(age)
                except ValueError:
                    print(f"Skipping row {row_counter} due to invalid age value: {age}")
                    continue

                # Generate UUID for each row
                user_id = str(uuid.uuid4())
                data.append((user_id, name, email, age))
        
        print(f"Data loaded successfully from {file_path}")
        print(f"Total rows loaded: {len(data)}")
    except Exception as e:
        print(f"Error loading CSV file: {e}")
    
    return data


# Main function to set up database, table, and insert data
def main():
    """Set up the database, table, and insert data from the CSV."""
    try:
        # Step 1: Connect to the MySQL server and create the database if not exists
        connection = connect_db()
        if connection is None:
            print("Could not connect to the database")
            return
        create_database(connection)  # Create database if not exists
        connection.close()  # Close connection to server
        
        # Step 2: Connect to the specific database and create the table if not exists
        connection = connect_to_prodev()
        create_table(connection)  # Create the table if not exists
        
        # Step 3: Load data from CSV and insert into the database
        file_path = "user_data.csv"  # Specify your CSV file path
        data = load_data_from_csv(file_path)
        
        if data:  # Only insert if there's data
            insert_data(connection, data)  # Insert data into the user_data table
        else:
            print("No data to insert.")
        
        connection.close()  # Close the database connection

    except mysql.connector.Error as err:
        print(f"Error: {err}")
    except Exception as e:
        print(f"Unexpected error: {e}")

# Run the script
if __name__ == "__main__":
    main()
