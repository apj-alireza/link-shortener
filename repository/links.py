import mysql.connector
from models.links import Link
from mysql.connector.errors import DatabaseError
from pydantic import BaseModel, Field, ConfigDict
from typing import List


class InvalidLinkID(DatabaseError):
    pass


class RepoLinkModel(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    link_id: str = Field(alias="id")
    destination: str = Field(alias="destination_url")
    slug: str = Field(alias="slug")


class LinksRepository():
    def __init__(self, conn: mysql.connector.MySQLConnection):
        self.conn = conn

    def CreateLink(self, user_id: int, destination: str, slug: str):
        cursor = self.conn.cursor()
        cursor.execute(
            f'INSERT INTO links(user_id,destination_url,slug) VALUES ("{user_id}","{destination}","{slug}")')

    def GetLinks(self, user_id: int) -> List[Link]:
        cursor = self.conn.cursor(dictionary=True)
        cursor.execute(
            f'SELECT BIN_TO_UUID(id) AS id,destination_url,slug FROM links WHERE user_id = {user_id}')
        rows = cursor.fetchall()

        result = [RepoLinkModel.model_validate(row)for row in rows]

        linkEntityList: List[Link] = []
        for i in result:
            j = Link(
                link_id=i.link_id,
                destination_url=i.destination,
                slug=i.slug
            )
            linkEntityList.append(j)
        return linkEntityList

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
                raise InvalidLinkID
            else:
                raise DatabaseError
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
                raise InvalidLinkID
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
            if row is None:
                raise DatabaseError
            else:
                url_str = str(row[0])
                return url_str
        except mysql.connector.Error as err:
            raise err
        finally:
            cursor.close()
