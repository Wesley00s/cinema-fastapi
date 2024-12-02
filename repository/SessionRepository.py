from typing import Optional, Dict

from database.Connection import Connection
from model.Session import Session


class SessionRepository:
    @staticmethod
    def save(session: Session) -> bool:
        db = Connection()
        try:
            db.connect()
            cursor = db.get_cursor()
            if cursor:
                sql = """
                INSERT INTO session (movie_id, room_id, start_time, end_time, price, language, subtitles, create_at, update_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """

                values = (session.movie_id, session.room_id, session.start_time, session.end_time, session.price, session.language, session.subtitles, session.create_at, session.update_at)

                cursor.execute(sql, values)
                db.connection.commit()
                return True

        except Exception as e:
            print(f'An exception occurred: {e}')
            return False

        finally:
            db.close()

    @staticmethod
    def get_by_id(id: int) -> Optional[Dict]:
        db = Connection()
        try:
            db.connect()
            cursor = db.get_cursor()
            if cursor:
                sql = """
                SELECT * FROM session WHERE id = ?
                """
                cursor.execute(sql, (id,))
                row = cursor.fetchone()
                if row:
                    columns = [column[0] for column in cursor.description]
                    return dict(zip(columns, row))
                return None

        except Exception as e:
            db.connection.rollback()
            print(f'An exception occurred: {e}')
            return None

        finally:
            db.close()

    @staticmethod
    def get_all() -> Optional[list]:
        db = Connection()
        try:
            db.connect()
            cursor = db.get_cursor()
            if cursor:
                sql = """
                SELECT * FROM session
                """

                cursor.execute(sql)
                rows = cursor.fetchall()
                columns = [desc[0] for desc in cursor.description]
                result = [dict(zip(columns, row)) for row in rows]
                return result
            return None
        except Exception as e:
            db.connection.rollback()
            print(f'An exception occurred: {e}')
            return None
        finally:
            db.close()

    @staticmethod
    def update(id: int, session: Session) -> bool:
        db = Connection()
        try:
            db.connect()
            cursor = db.get_cursor()
            if cursor:
                sql1 = """
                SELECT * FROM session WHERE id = ?
                """
                cursor.execute(sql1, (id,))
                row = cursor.fetchone()

                if not row:
                    print(f"No session found with id {id}.")
                    return False

                columns = [column[0] for column in cursor.description]
                existing_session = dict(zip(columns, row))

                update_fields = []
                values = []

                if session.movie_id and session.movie_id != existing_session['movie_id']:
                    update_fields.append("movie_id = ?")
                    values.append(session.movie_id)
                if session.room_id and session.room_id != existing_session['room_id']:
                    update_fields.append("room_id = ?")
                    values.append(session.room_id)
                if session.language and session.language != existing_session['language']:
                    update_fields.append("language = ?")
                    values.append(session.language)
                if session.subtitles and session.subtitles != existing_session['subtitles']:
                    update_fields.append("subtitles = ?")
                    values.append(session.subtitles)
                if session.start_time and session.start_time != existing_session['start_time']:
                    update_fields.append("start_time = ?")
                    values.append(session.start_time)
                if session.end_time and session.end_time != existing_session['end_time']:
                    update_fields.append("end_time = ?")
                    values.append(session.end_time)
                if session.price and session.price != existing_session['price']:
                    update_fields.append("price = ?")
                    values.append(session.price)
                if session.update_at and session.update_at != existing_session['update_at']:
                    update_fields.append("update_at = ?")
                    values.append(session.update_at)

                if not update_fields:
                    print(f"No changes detected for room with id {id}.")
                    return False

                set_clause = ", ".join(update_fields)
                sql2 = f"""
                    UPDATE room
                    SET {set_clause}
                    WHERE id = ?
                """

                values.append(id)

                cursor.execute(sql2, values)
                db.connection.commit()
                print(f"Room with id {id} updated successfully.")
                return True

        except Exception as e:
            db.connection.rollback()
            print(f"Error updating customer with id {id}: {e}")
            return False
        finally:
            db.close()

    @staticmethod
    def delete(id: int) -> bool:
        db = Connection()
        try:
            db.connect()
            cursor = db.get_cursor()
            if cursor:
                sql = """
                DELETE FROM session WHERE id = ?
                """

                cursor.execute(sql, (id,))
                db.connection.commit()
                return True

        except Exception as e:
            db.connection.rollback()
            print(f'An exception occurred to delete session by id')
            return False

        finally:
            db.close()