import mysql.connector
from models.links import Link
from mysql.connector.errors import DatabaseError
from mysql.connector import errorcode


class InvalidLinkID(DatabaseError):
    pass


class LinksRepository():
    def __init__(self, conn: mysql.connector.MySQLConnection):
        self.conn = conn

    def CreateLink(self, user_id: int, destination: str, slug: str):
        cursor = self.conn.cursor()
        cursor.execute(
            f'INSERT INTO links(user_id,destination_url,slug) VALUES ("{user_id}","{destination}","{slug}")')

    def GetLinks(self, user_id: int) -> Link:
        cursor = self.conn.cursor()
        cursor.execute(
            f'SELECT BIN_TO_UUID(id) AS id,destination_url,slug FROM links WHERE user_id = {user_id}')
        LinksResualt = cursor.fetchall()
        List = []
        for i in LinksResualt:
            j = Link(i[0], i[1], i[2])
            List.append(j)
        return List

    def UpdateLinks(self, user_id, link_id, NewDest: str):
        cursor = self.conn.cursor()
        try:
            cursor.execute(
                """
        UPDATE links
        SET destination_url = %s
        WHERE id = UUID_TO_BIN(%s) AND user_id = %s
        """,
                (NewDest, link_id, user_id)
            )
        except mysql.connector.errors.Error as err:
            if err.errno == 1411:
                raise InvalidLinkID from err
        finally:
            if cursor.rowcount == 0:
                raise InvalidLinkID
            cursor.close()

    def DeleteLinks(self, user_id, link_id):
        cursor = self.conn.cursor()
        try:
            cursor.execute(
                'DELETE FROM links WHERE id = UUID_TO_BIN(%s) AND user_id = %s', (link_id, user_id))
        except mysql.connector.errors.Error as err:
            if err.errno == 1411:
                raise InvalidLinkID from err
        finally:
            if cursor.rowcount == 0:
                raise InvalidLinkID
            cursor.close()

    def GetLinkBySlug(self, slug: str):
        cursor = self.conn.cursor()
        try:
            cursor.execute(
                'SELECT destination_url from links WHERE slug = %s', (slug,))
            row = cursor.fetchone()
            print("ROW", row)
            print(type(row))
            if row is None:
                raise InvalidLinkID()
            else:
                url_str = str(row[0])
                return url_str
        except mysql.connector.Error as err:
            raise err
        finally:
            cursor.close()
