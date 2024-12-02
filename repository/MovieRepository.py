from typing import Optional, Dict

import bcrypt

from database.Connection import Connection
from model.Movie import Movie


class MovieRepository:
    @staticmethod
    def save(movie: Movie):
        db = Connection()
        try:
            db.connect()
            cursor = db.get_cursor()
            if cursor:
                sql = """
                 INSERT INTO movie (title, genre, synopsis, duration, age_rating, director, release_date, create_at, update_at)
                 VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                 """

                values = (
                    movie.title,
                    movie.genre,
                    movie.synopsis,
                    movie.duration,
                    movie.age_rating,
                    movie.director,
                    movie.release_date,
                    movie.create_at,
                    movie.update_at
                    )
                cursor.execute(sql, values)
                db.connection.commit()
                return True

        except Exception as e:
            db.connection.rollback()
            print(f'An exception occurred on save movie: {e}')
            return False
        finally:
            db.close()

    @staticmethod
    def update(id: int, movie: Movie) -> bool:
        db = Connection()
        try:
            db.connect()
            cursor = db.get_cursor()
            if cursor:
                sql1 = """
                SELECT * FROM movie WHERE id = ?
                """
                cursor.execute(sql1, (id,))
                row = cursor.fetchone()

                if not row:
                    print(f"No movie found with id {id}.")
                    return False

                columns = [column[0] for column in cursor.description]
                existing_movie = dict(zip(columns, row))

                update_fields = []
                values = []

                if movie.title and movie.title != existing_movie['title']:
                    update_fields.append('title = ?')
                    values.append(movie.title)
                if movie.genre and movie.genre != existing_movie['genre']:
                    update_fields.append('genre = ?')
                    values.append(movie.genre)
                if movie.synopsis and movie.synopsis != existing_movie['synopsis']:
                    update_fields.append('synopsis = ?')
                    values.append(movie.synopsis)
                if movie.duration and movie.duration != existing_movie['duration']:
                    update_fields.append('duration = ?')
                    values.append(movie.duration)
                if movie.age_rating and movie.age_rating != existing_movie['age_rating']:
                    update_fields.append('age_rating = ?')
                    values.append(movie.age_rating)
                if movie.director and movie.director != existing_movie['director']:
                    update_fields.append('director = ?')
                    values.append(movie.director)
                if movie.release_date and movie.release_date != existing_movie['release_date']:
                    update_fields.append('release_date = ?')
                    values.append(movie.release_date)
                if movie.create_at and movie.create_at != existing_movie['create_at']:
                    update_fields.append('create_at = ?')
                    values.append(movie.create_at)
                if movie.update_at and movie.update_at != existing_movie['update_at']:
                    update_fields.append('update_at = ?')
                    values.append(movie.update_at)

                if not update_fields:
                    print(f"No changes detected for customer with id {id}.")
                    return False

                set_clause = ", ".join(update_fields)
                sql2 = f"""
                    UPDATE movie
                    SET {set_clause}
                    WHERE id = ?
                """

                values.append(id)

                cursor.execute(sql2, values)
                db.connection.commit()
                print(f"Movie with id {id} updated successfully.")
                return True

        except Exception as e:
            db.connection.rollback()
            print(f'An exception occurred on update movie: {e}')
            return False
        finally:
            db.close()

    @staticmethod
    def get_by_id(id: int) -> Optional[Dict]:
        try:
            with Connection() as db:
                db.connect()
                cursor = db.get_cursor()
                if cursor:
                    sql = "SELECT * FROM movie WHERE id = ?"
                    cursor.execute(sql, (id,))
                    row = cursor.fetchone()
                    if row:
                        columns = [column[0] for column in cursor.description]
                        return dict(zip(columns, row))
                return None
        except Exception as e:
            print(f"An exception occurred while fetching the movie by id {id}: {e}")
            return None

    @staticmethod
    def get_all() -> Optional[list[Dict]]:
        db = Connection()
        try:
            db.connect()
            cursor = db.get_cursor()
            if cursor:
                sql = "SELECT * FROM movie"
                cursor.execute(sql)
                rows = cursor.fetchall()

                columns = [desc[0] for desc in cursor.description]
                result = [dict(zip(columns, row)) for row in rows]
                return result
        except Exception as e:
            print(f"An exception occurred while fetching movies: {e}")
            return None
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
                DELETE FROM movie WHERE id = ?
                """

                cursor.execute(sql, (id,))
                db.connection.commit()
                return True

        except Exception as e:
            db.connection.rollback()
            print(f'An exception occurred to delete movie by id')
            return False

        finally:
            db.close()