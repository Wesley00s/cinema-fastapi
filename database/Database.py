from database.Connection import Connection


class Database:
    @staticmethod
    def create_customer_table():
        db = Connection()
        try:
            db.connect()
            cursor = db.get_cursor()
            if cursor:
                sql = """
                CREATE TABLE IF NOT EXISTS customer (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    email TEXT NOT NULL UNIQUE,
                    password TEXT NOT NULL,
                    first_name TEXT NOT NULL,
                    last_name TEXT NOT NULL,
                    address TEXT NOT NULL,
                    city TEXT NOT NULL,
                    state TEXT NOT NULL,
                    zip_code TEXT NOT NULL,
                    country TEXT NOT NULL,
                    role TEXT NOT NULL,
                    age INTEGER NOT NULL
                );
                """
                cursor.execute(sql)
        except Exception as e:
            print(f'An error occurred while creating table: {e}')
        finally:
            db.close()

    @staticmethod
    def create_admin_table():
        db = Connection()
        try:
            db.connect()
            cursor = db.get_cursor()
            if cursor:
                sql = """
                        CREATE TABLE IF NOT EXISTS admin (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        email TEXT NOT NULL UNIQUE,
                        password TEXT NOT NULL,
                        first_name TEXT NOT NULL,
                        last_name TEXT NOT NULL,
                        address TEXT NOT NULL,
                        city TEXT NOT NULL,
                        state TEXT NOT NULL,
                        zip_code TEXT NOT NULL,
                        country TEXT NOT NULL,
                        role TEXT NOT NULL
                        );
                        """
                cursor.execute(sql)
        except Exception as e:
                print(f'An error occurred while creating table: {e}')
        finally:
            db.close()

    @staticmethod
    def create_movie_table():
        db = Connection()
        try:
            db.connect()
            cursor = db.get_cursor()
            if cursor:
                sql = """
                CREATE TABLE IF NOT EXISTS movie (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                genre TEXT NOT NULL,
                synopsis TEXT NOT NULL,
                duration INTEGER NOT NULL,
                age_rating INTEGER NOT NULL,
                director TEXT NOT NULL,
                release_date TEXT NOT NULL,
                create_at TIMESTAMP NOT NULL,
                update_at TIMESTAMP NOT NULL
                );
                """
                cursor.execute(sql)

        except Exception as e:
            print(f'An error occurred while creating table: {e}')
        finally:
            db.close()

    @staticmethod
    def create_room_table():
        db = Connection()
        try:
            db.connect()
            cursor = db.get_cursor()
            if cursor:
                sql = """
                CREATE TABLE IF NOT EXISTS room (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                number INTEGER NOT NULL,
                capacity INTEGER NOT NULL,
                create_at TIMESTAMP NOT NULL,
                update_at TIMESTAMP NOT NULL
                );
                """
                cursor.execute(sql)

        except Exception as e:
            print(f'An error occurred while creating table: {e}')
        finally:
            db.close()

    @staticmethod
    def create_session_table():
        db = Connection()
        try:
            db.connect()
            cursor = db.get_cursor()
            if cursor:
                sql = """
                CREATE TABLE IF NOT EXISTS session (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                movie_id INTEGER NOT NULL REFERENCES customer (id),
                room_id INTEGER NOT NULL REFERENCES movie (id),
                start_time TIMESTAMP NOT NULL,
                end_time TIMESTAMP NOT NULL,
                price REAL NOT NULL,
                language TEXT NOT NULL,
                subtitles BOOLEAN NOT NULL,
                create_at TIMESTAMP NOT NULL,
                update_at TIMESTAMP NOT NULL
                );
                """
                cursor.execute(sql)

        except Exception as e:
            print(f'An error occurred while creating table: {e}')
        finally:
            db.close()

    @staticmethod
    def create_ticket_table():
        db = Connection()
        try:
            db.connect()
            cursor = db.get_cursor()
            if cursor:
                sql = """
                CREATE TABLE IF NOT EXISTS ticket (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id INTEGER NOT NULL REFERENCES session (id),
                user_id INTEGER NOT NULL REFERENCES customer (id),
                price REAL NOT NULL,
                status TEXT NOT NULL,
                create_at TIMESTAMP NOT NULL,
                update_at TIMESTAMP NOT NULL
                );
                """
                cursor.execute(sql)

        except Exception as e:
            print(f'An error occurred while creating table: {e}')
        finally:
            db.close()

    @staticmethod
    def create_all_tables():
        Database.create_customer_table()
        Database.create_admin_table()
        Database.create_movie_table()
        Database.create_room_table()
        Database.create_session_table()
        Database.create_ticket_table()
