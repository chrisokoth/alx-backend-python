import mysql.connector

def connect_to_prodev():
    """Connect to the MySQL database."""
    return mysql.connector.connect(
        host="localhost",  
        user="root",       
        password="okothee07",  
        database="ALX_prodev"
    )

def paginate_users(page_size, offset):
    """Fetch users from the database with pagination."""
    connection = connect_to_prodev()
    cursor = connection.cursor(dictionary=True)  # Use dictionary cursor to get rows as dict
    cursor.execute(f"SELECT * FROM user_data LIMIT {page_size} OFFSET {offset}")
    rows = cursor.fetchall()
    connection.close()
    return rows

def lazy_paginate(page_size):
    """Generator function to lazily load users in pages."""
    offset = 0
    while True:
        # Fetch the users in the current page
        page = paginate_users(page_size, offset)
        if not page:
            break  # Stop if no users are returned (end of data)
        yield page  # Yield the current page of users
        offset += page_size  # Update the offset for the next page
