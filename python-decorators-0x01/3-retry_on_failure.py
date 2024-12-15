import time
import sqlite3
import functools

def with_db_connection(func):
    """Decorator to handle database connection automatically."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect('users.db')  
        try:
            result = func(conn, *args, **kwargs)  
        finally:
            conn.close()  
        return result
    return wrapper

def retry_on_failure(retries=3, delay=2):
    """Decorator to retry a function on failure due to transient errors."""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            attempts = 0
            while attempts < retries:
                try:
                    return func(*args, **kwargs)  
                except sqlite3.OperationalError as e:
                    attempts += 1
                    print(f"Attempt {attempts}/{retries} failed with error: {e}")
                    if attempts == retries:
                        print("All retries failed. Raising the exception.")
                        raise  
                    time.sleep(delay) 
        return wrapper
    return decorator

@with_db_connection
@retry_on_failure(retries=3, delay=1)
def fetch_users_with_retry(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    return cursor.fetchall()

try:
    users = fetch_users_with_retry()
    print(users)
except sqlite3.OperationalError:
    print("Fetching users failed after retries.")
