import sqlite3

class Connection:
    def __init__(self, database='database/cinema.db'):
        self.database = database
        self.connection = None

    def connect(self):
        try:
            self.connection = sqlite3.connect(self.database)
            print(f"Connected to SQLite Database: {self.database}")
        except sqlite3.Error as e:
            print(f"Error connecting to SQLite: {e}")
            self.connection = None

    def get_cursor(self):

        if self.connection:
            return self.connection.cursor()
        else:
            print("No active SQLite connection. Call connect() first.")
            return None

    def close(self):

        if self.connection:
            self.connection.close()
            print("SQLite connection closed.")
        else:
            print("No active SQLite connection to close.")

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.connection:
            self.close()
