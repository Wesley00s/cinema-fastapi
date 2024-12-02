from typing import Optional, Dict

from database.Connection import Connection
from model.Room import Room


class RoomRepository:
    @staticmethod
    def save(room: Room) -> bool:
        db = Connection()
        try:
            db.connect()
            cursor = db.get_cursor()

            if cursor:
                sql = """
                    INSERT INTO room (number, capacity, create_at, update_at)
                    VALUES (?, ?, ?, ?)
                """

                values = (room.number, room.capacity, room.create_at, room.update_at)
                cursor.execute(sql, values)
                db.connection.commit()
                return True

        except Exception as e:
            db.connection.rollback()
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
                SELECT * FROM room WHERE id = ?
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
                SELECT * FROM room
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
    def update(id: int, room: Room) -> bool:
        db = Connection()
        try:
            db.connect()
            cursor = db.get_cursor()
            if cursor:
                sql1 = """
                SELECT * FROM room WHERE id = ?
                """
                cursor.execute(sql1, (id,))
                row = cursor.fetchone()

                if not row:
                    print(f"No customer found with id {id}.")
                    return False

                columns = [column[0] for column in cursor.description]
                existing_room = dict(zip(columns, row))

                update_fields = []
                values = []

                if room.number and room.number != existing_room['number']:
                    update_fields.append("number = ?")
                    values.append(room.number)
                if room.capacity and room.capacity != existing_room['capacity']:
                    update_fields.append("capacity = ?")
                    values.append(room.capacity)
                if room.update_at and room.update_at != existing_room['update_at']:
                    update_fields.append("update_at = ?")
                    values.append(room.update_at)

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
                DELETE FROM room WHERE id = ?
                """

                cursor.execute(sql, (id,))
                db.connection.commit()
                return True

        except Exception as e:
            db.connection.rollback()
            print(f'An exception occurred to delete room by id')
            return False

        finally:
            db.close()
