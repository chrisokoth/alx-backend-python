
import sqlite3
import functools

def with_db_connection(func):
    """Decorator to handle database connection automatically."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect('users.db')  # Open the database connection
        try:
            result = func(conn, *args, **kwargs)  # Pass connection to wrapped function
        finally:
            conn.close()  # Ensure the connection is closed after execution
        return result
    return wrapper

def transactional(func):
    """Decorator to manage database transactions."""
    @functools.wraps(func)
    def wrapper(conn, *args, **kwargs):
        try:
            result = func(conn, *args, **kwargs)  # Execute the function
            conn.commit()  # Commit the transaction if no errors occur
            return result
        except Exception as e:
            conn.rollback()  # Rollback the transaction if an error occurs
            raise e  # Re-raise the exception to signal the failure
    return wrapper

@with_db_connection
@transactional
def update_user_email(conn, user_id, new_email):
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET email = ? WHERE id = ?", (new_email, user_id))

# Update user's email with automatic transaction handling
update_user_email(user_id=1, new_email='Crawford_Cartwright@hotmail.com')
