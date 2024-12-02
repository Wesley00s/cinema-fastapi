from datetime import datetime
from typing import Optional, Dict, List

from database.Connection import Connection
from model.Ticket import Ticket


class TicketRepository:
    @staticmethod
    def save(ticket: Ticket):
        db = Connection()
        try:
            db.connect()
            cursor = db.get_cursor()
            if cursor:
                sql = """
                INSERT INTO ticket (session_id, customer_id, price, status, create_at, update_at)
                VALUES (?, ?, ?, ?, ?, ?)
                """

                values = (ticket.session_id, ticket.customer_id, ticket.price, ticket.status, ticket.create_at, ticket.update_at)
                cursor.execute(sql, values)
                db.connection.commit()
                return True
        except Exception as e:
            db.connection.rollback()
            print(f'An exception occurred while saving the ticket: {e}')
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
                SELECT * FROM ticket WHERE id = ?
                """
                cursor.execute(sql, (id,))
                row = cursor.fetchone()
                if row:
                    columns = [column[0] for column in cursor.description]
                    return dict(zip(columns, row))
                return None

        except Exception as e:
            db.connection.rollback()
            print(f'An exception occurred while getting the ticket: {e}')
            return None

        finally:
            db.close()

    @staticmethod
    def get_all() -> Optional[list[Dict]]:
        db = Connection()
        try:
            db.connect()
            cursor = db.get_cursor()
            if cursor:
                sql = """
                SELECT * FROM ticket
                """
                cursor.execute(sql)
                rows = cursor.fetchall()
                columns = cursor.description
                result = [dict(zip(columns, row)) for row in rows]
                return result
            return None
        except Exception as e:
            db.connection.rollback()
            print(f'An exception occurred while getting the ticket: {e}')
            return None
        finally:
            db.close()

    @staticmethod
    def update(id: int, ticket: Ticket):
        db = Connection()
        try:
            db.connect()
            cursor = db.get_cursor()
            if cursor:
                sql1 = """
                SELECT * FROM ticket WHERE id = ?
                """
                cursor.execute(sql1, (id,))
                row = cursor.fetchone()
                if not row:
                    print(f"No session found with id {id}.")
                    return False

                columns = [column[0] for column in cursor.description]
                existing_ticket = dict(zip(columns, row))

                update_fields = []
                values = []

                if ticket.session_id != existing_ticket.get('session_id'):
                    update_fields.append('session_id')
                    values.append(ticket.session_id)
                if ticket.customer_id != existing_ticket.get('customer_id'):
                    update_fields.append('customer_id')
                    values.append(ticket.customer_id)
                if ticket.price != existing_ticket.get('price'):
                    update_fields.append('price')
                    values.append(ticket.price)
                if ticket.status != existing_ticket.get('status'):
                    update_fields.append('status')
                    values.append(existing_ticket.get('status'))
                if ticket.update_at != existing_ticket.get('update_at'):
                    update_fields.append('update_at')
                    values.append(existing_ticket.get('update_at'))

                if not update_fields:
                    print(f"No changes detected for ticket with id {id}.")
                    return False

                set_clause = ", ".join(update_fields)
                sql2 = f"""
                    UPDATE ticket
                    SET {set_clause}
                    WHERE id = ?
                """

                values.append(id)

                cursor.execute(sql2, values)
                db.connection.commit()
                print(f"Ticket with id {id} updated successfully.")
                return True
        except Exception as e:
            db.connection.rollback()
            print(f'An exception occurred while updating the ticket: {e}')
            return False
        finally:
            db.close()

    @staticmethod
    def delete(id: int):
        db = Connection()
        try:
            db.connect()
            cursor = db.get_cursor()
            if cursor:
                sql = """
                DELETE FROM ticket WHERE id = ?
                """
                cursor.execute(sql, (id,))
                db.connection.commit()
                return True
        except Exception as e:
            db.connection.rollback()
            print(f'An exception occurred while deleting ticket: {e}')
            return False
        finally:
            db.close()
