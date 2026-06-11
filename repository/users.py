from mysql.connector.errors import DatabaseError
import mysql.connector
from models.user import User
from pydantic import BaseModel, Field, ConfigDict


class DuplicateError(DatabaseError):
    pass


class ConnectionError(DatabaseError):
    pass


class UserNotfound(Exception):
    pass


class UserRepoMolel(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    id: int = Field(alias="id")
    username: str = Field(alias="username")
    password: str = Field(alias="passwords")


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
        cursor = self.conn.cursor(dictionary=True)

        cursor.execute(
            f"SELECT * FROM users WHERE username = '{username}'")
        row = cursor.fetchone()
        if row is None:
            cursor.close()
            raise UserNotfound("User not found!")
        else:
            user_result = UserRepoMolel.model_validate(row)
        user = User(
            user_id=user_result.id, Username=user_result.username, Password=user_result.password)

        cursor.close()
        return user
