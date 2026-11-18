import psycopg2
from flask import g

from helpers.application import app
from helpers.enviroment import enviroment

DATABASE_NAME = enviroment.get("DB_NAME")
DATABASE_HOST = enviroment.get("DB_HOST")
DATABASE_PORT = enviroment.get("DB_PORT")
DATABASE_USER = enviroment.get("DB_USER")
DATABASE_PASSWORD = enviroment.get("DB_PASSWORD")


def get_connection():
    conn = getattr(g, '_database', None)
    if conn is None:
        conn = g._database = psycopg2.connect(
            database=DATABASE_NAME, user=DATABASE_USER, password=DATABASE_PASSWORD, host=DATABASE_HOST, port=DATABASE_PORT)
    return conn


@app.teardown_appcontext
def close_connection(exception):
    conn = getattr(g, '_database', None)
    if conn is not None:
        conn.close()
