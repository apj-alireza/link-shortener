from mysql.connector.errors import DatabaseError
import mysql.connector
from models.user import User


class DuplicateError(DatabaseError):
    pass


class ConnectionError(DatabaseError):
    pass


class UserNotfound(Exception):
    pass


class UserRepository():
    def __init__(self, conn: mysql.connector.MySQLConnection):
        self.conn = conn

    def CreateUser(self, username, password: str):

        cursor = self.conn.cursor()
        try:
            cursor.execute(
                f'INSERT INTO users(username,passwords) Values ("{username}","{password}")')
        except mysql.connector.errors.Error as err:
            if err.errno == 1062:
                raise DuplicateError("This username already exist!") from err
            else:
                raise ConnectionError("DB connection failed!")
        finally:
            cursor.close()

    def GetUser(self, username: str) -> User:
        cursor = self.conn.cursor()

        cursor.execute(
            f"SELECT * FROM users WHERE username = '{username}'")
        userResult = cursor.fetchone()

        if userResult is None:
            cursor.close()
            raise UserNotfound("User not found!")

        user = User(
            user_id=userResult[0], Username=userResult[1], Password=userResult[2])

        cursor.close()
        return user
