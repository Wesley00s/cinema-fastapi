from typing import Optional, Dict

import bcrypt

from database.Connection import Connection
from model.Customer import Customer


class CustomerRepository:
    @staticmethod
    def save(customer: Customer) -> bool:
        db = Connection()
        try:
            hashed_password = bcrypt.hashpw(customer.password.encode('utf-8'), bcrypt.gensalt())
            db.connect()
            cursor = db.get_cursor()
            if cursor:
                sql = """
                       INSERT INTO customer (email, password, first_name, last_name, address, city, state, zip_code, country, role, age)
                       VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                       """

                values = (customer.email, hashed_password.decode('utf-8'), customer.first_name, customer.last_name, customer.address,
                          customer.city, customer.state, customer.zip_code, customer.country, customer.role.value, customer.age)

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
    def update(id: int, customer: Customer) -> Optional[Customer]:
        db = Connection()
        try:
            db.connect()
            cursor = db.get_cursor()
            if cursor:
                sql1 = """
                SELECT * FROM customer WHERE id = ?
                """
                cursor.execute(sql1, (id,))
                row = cursor.fetchone()

                if not row:
                    print(f"No customer found with id {id}.")
                    return False

                columns = [column[0] for column in cursor.description]
                existing_customer = dict(zip(columns, row))

                update_fields = []
                values = []

                if customer.password and customer.password != existing_customer['password']:
                    update_fields.append("password = ?")
                    values.append(customer.password)
                if customer.first_name and customer.first_name != existing_customer['first_name']:
                    update_fields.append("first_name = ?")
                    values.append(customer.first_name)
                if customer.last_name and customer.last_name != existing_customer['last_name']:
                    update_fields.append("last_name = ?")
                    values.append(customer.last_name)
                if customer.address and customer.address != existing_customer['address']:
                    update_fields.append("address = ?")
                    values.append(customer.address)
                if customer.city and customer.city != existing_customer['city']:
                    update_fields.append("city = ?")
                    values.append(customer.city)
                if customer.state and customer.state != existing_customer['state']:
                    update_fields.append("state = ?")
                    values.append(customer.state)
                if customer.zip_code and customer.zip_code != existing_customer['zip_code']:
                    update_fields.append("zip_code = ?")
                    values.append(customer.zip_code)
                if customer.country and customer.country != existing_customer['country']:
                    update_fields.append("country = ?")
                    values.append(customer.country)
                if customer.age and customer.age != existing_customer['age']:
                    update_fields.append("age = ?")
                    values.append(customer.age)

                if not update_fields:
                    print(f"No changes detected for customer with id {id}.")
                    return False

                set_clause = ", ".join(update_fields)
                sql2 = f"""
                    UPDATE customer
                    SET {set_clause}
                    WHERE id = ?
                """

                values.append(id)

                cursor.execute(sql2, values)
                db.connection.commit()
                print(f"Customer with id {id} updated successfully.")
                return True

        except Exception as e:
            db.connection.rollback()
            print(f"Error updating customer with id {id}: {e}")
            return False

        finally:
            db.close()

    @staticmethod
    def get_by_id(id: int) -> Optional[Dict]:
        try:
            with Connection() as db:
                cursor = db.get_cursor()
                if cursor:
                    sql = "SELECT * FROM customer WHERE id = ?"
                    cursor.execute(sql, (id,))
                    row = cursor.fetchone()
                    if row:
                        columns = [column[0] for column in cursor.description]
                        return dict(zip(columns, row))
                return None
        except Exception as e:
            print(f"An exception occurred while fetching the customer by id {id}: {e}")
            return None

    @staticmethod
    def delete(id: int) -> bool:
        db = Connection()
        try:
            db.connect()
            cursor = db.get_cursor()
            if cursor:
                sql = """
                DELETE FROM customer WHERE id = ?
                """

                cursor.execute(sql, (id,))
                db.connection.commit()
                return True

        except Exception as e:
            db.connection.rollback()
            print(f'An exception occurred to delete user by id')
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
                SELECT password, first_name, last_name, role FROM customer WHERE email = ?
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
            print(f'An exception occurred to authenticate user by email, {e}')
            return None
        finally:
            db.close()
