import sqlite3

class ExecuteQuery:
    def __init__(self, db_name, query, params=None):
        """
        Initialize the context manager with database name, query, and parameters.
        """
        self.db_name = db_name
        self.query = query
        self.params = params
        self.connection = None
        self.cursor = None

    def __enter__(self):
        """
        Establish a database connection and execute the query.
        """
        self.connection = sqlite3.connect(self.db_name)
        self.cursor = self.connection.cursor()
        self.cursor.execute(self.query, self.params or [])
        return self.cursor.fetchall()

    def __exit__(self, exc_type, exc_value, traceback):
        """
        Close the database connection and handle exceptions if any.
        """
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()

query = "SELECT * FROM users WHERE age > ?"
param = (25,)

# Use the context manager to execute the query
with ExecuteQuery('users.db', query, param) as results:
    for row in results:
        print(row)
