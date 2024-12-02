from typing import Optional, Dict

import bcrypt

from database.Connection import Connection
from model.Admin import Admin


class AdminRepository:
    @staticmethod
    def save(admin: Admin):
        db = Connection()
        try:
            hashed_password = bcrypt.hashpw(admin.password.encode('utf-8'), bcrypt.gensalt())
            db.connect()
            cursor = db.get_cursor()
            if cursor:
                sql = """
                       INSERT INTO admin (email, password, first_name, last_name, address, city, state, zip_code, country, role)
                       VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                       """

                values = (admin.email, hashed_password.decode('utf-8'), admin.first_name, admin.last_name, admin.address,
                          admin.city, admin.state, admin.zip_code, admin.country, admin.role.value)

                cursor.execute(sql, values)
                db.connection.commit()
                return True

        except Exception as e:
            db.connection.rollback()
            print(f"Error: {e}")
            return False

        finally:
            db.close()

    @staticmethod
    def update(id: int, admin: Admin):
        db = Connection()
        try:
            db.connect()
            cursor = db.get_cursor()
            if cursor:
                sql1 = """
                SELECT * FROM admin WHERE id = ?
                """
                cursor.execute(sql1, (id,))
                row = cursor.fetchone()

                if not row:
                    print(f"No admin found with id {id}.")
                    return False

                columns = [column[0] for column in cursor.description]
                existing_admin = dict(zip(columns, row))

                update_fields = []
                values = []

                if admin.password and admin.password != existing_admin['password']:
                    update_fields.append("password = ?")
                    values.append(admin.password)
                if admin.first_name and admin.first_name != existing_admin['first_name']:
                    update_fields.append("first_name = ?")
                    values.append(admin.first_name)
                if admin.last_name and admin.last_name != existing_admin['last_name']:
                    update_fields.append("last_name = ?")
                    values.append(admin.last_name)
                if admin.address and admin.address != existing_admin['address']:
                    update_fields.append("address = ?")
                    values.append(admin.address)
                if admin.city and admin.city != existing_admin['city']:
                    update_fields.append("city = ?")
                    values.append(admin.city)
                if admin.state and admin.state != existing_admin['state']:
                    update_fields.append("state = ?")
                    values.append(admin.state)
                if admin.zip_code and admin.zip_code != existing_admin['zip_code']:
                    update_fields.append("zip_code = ?")
                    values.append(admin.zip_code)
                if admin.country and admin.country != existing_admin['country']:
                    update_fields.append("country = ?")
                    values.append(admin.country)

                if not update_fields:
                    print(f"No changes detected for admin with id {id}.")
                    return False

                set_clause = ", ".join(update_fields)
                sql2 = f"""
                    UPDATE admin
                    SET {set_clause}
                    WHERE id = ?
                """

                values.append(id)

                cursor.execute(sql2, values)
                db.connection.commit()
                print(f"Admin with id {id} updated successfully.")
                return True

        except Exception as e:
            db.connection.rollback()
            print(f"Error updating admin with id {id}: {e}")
            return False

        finally:
            db.close()

    @staticmethod
    def get_by_id(id: int):
        db = Connection()
        try:
            db.connect()
            cursor = db.get_cursor()
            if cursor:
                sql = """
                SELECT * FROM admin WHERE id = ?
                """

                cursor.execute(sql, (id,))
                row = cursor.fetchone()
                if row:
                    columns = [column[0] for column in cursor.description]
                    return dict(zip(columns, row))

                return None

        except Exception as e:
            db.connection.rollback()
            print(f'An exception occurred to get admin by id')
            return None
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
                DELETE FROM admin WHERE id = ?
                """

                cursor.execute(sql, (id,))
                db.connection.commit()
                return True

        except Exception as e:
            db.connection.rollback()
            print(f'An exception occurred to delete admin by id')
            return False

        finally:
            db.close()


    @staticmethod
    def authenticate(email: str, password: str) -> Optional[Dict]:
        db = Connection()
        try:
            db.connect()
            cursor = db.get_cursor()
            if cursor:
                sql = """
                SELECT password, first_name, last_name, role FROM admin WHERE email = ?
                """

                cursor.execute(sql, (email,))
                row = cursor.fetchone()
                if row:
                    stored_password, first_name, last_name, role = row
                    if bcrypt.checkpw(password.encode('utf-8'), stored_password.encode('utf-8')):
                        return {"name": f'{first_name} {last_name}', "role": role}
                return None
        except Exception as e:
            db.connection.rollback()
            print(f'An exception occurred to authenticate admin by email, {e}')
            return None
        finally:
            db.close()
