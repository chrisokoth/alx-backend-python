import mysql.connector

def connect_db():
    """Connect to the MySQL database."""
    return mysql.connector.connect(
        host="localhost",  
        user="root",       
        password="okothee07", 
        database="ALX_prodev"
    )

def stream_users_in_batches(batch_size):
    """Generator function to stream users in batches."""
    connection = connect_db()
    cursor = connection.cursor(dictionary=True)  # Use dictionary cursor to get rows as dict
    cursor.execute("SELECT user_id, name, email, age FROM user_data")
    
    # Fetch the rows in batches
    while True:
        batch = cursor.fetchmany(batch_size)
        if not batch:
            break
        yield batch

    cursor.close()
    connection.close()

def batch_processing(batch_size):
    """Process each batch to filter users over the age of 25."""
    for batch in stream_users_in_batches(batch_size):
        # Filter users over the age of 25 and yield them
        for user in batch:
            if user['age'] > 25:
                yield user
