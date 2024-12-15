from datetime import datetime
import sqlite3
import logging
import functools

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

def log_queries(func):
    """Decorator to log SQL queries before execution."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        query = kwargs.get('query') if 'query' in kwargs else args[0] if args else None
        if query:
            logging.info(f"Executing query: {query}")
        else:
            logging.warning("No SQL query provided to log.")
        return func(*args, **kwargs)
    return wrapper

@log_queries
def fetch_all_users(query):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results

# Fetch users and log the query
users = fetch_all_users(query="SELECT * FROM users")
print(users)
