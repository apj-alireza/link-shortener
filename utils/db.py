import mysql.connector
from mysql.connector import MySQLConnection
from utils.configs import DB_PASSWORD, DB_USER


def connectDB() -> MySQLConnection:
    cnx = mysql.connector.connect(user=DB_USER, password=DB_PASSWORD,
                                  host='127.0.0.1',
                                  database='link_shortener',
                                  autocommit=True
                                  )
    return cnx
