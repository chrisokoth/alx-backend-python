import sqlite3
import functools

# Cache dictionary to store query results
query_cache = {}

def with_db_connection(func):
    """Decorator to handle database connection automatically."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect('users.db')  # Open the database connection
        try:
            result = func(conn, *args, **kwargs)  # Pass connection to the wrapped function
        finally:
            conn.close()  # Ensure the connection is closed after execution
        return result
    return wrapper

def cache_query(func):
    """Decorator to cache query results based on the SQL query string."""
    @functools.wraps(func)
    def wrapper(conn, query, *args, **kwargs):
        if query in query_cache:
            print(f"Using cached result for query: {query}")
            return query_cache[query]
        
        print(f"Executing query and caching result: {query}")
        result = func(conn, query, *args, **kwargs)  # Execute the query
        query_cache[query] = result  # Cache the result
        return result
    return wrapper

@with_db_connection
@cache_query
def fetch_users_with_cache(conn, query):
    """Fetch users based on the SQL query."""
    cursor = conn.cursor()
    cursor.execute(query)
    return cursor.fetchall()

# First call will execute and cache the result
users = fetch_users_with_cache(query="SELECT * FROM users")
print(users)

# Second call will use the cached result
users_again = fetch_users_with_cache(query="SELECT * FROM users")
print(users_again)
