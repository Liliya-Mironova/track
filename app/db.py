import flask
import psycopg2
import psycopg2.extras
from instance import config


def get_connection():
    if not hasattr(flask.g, 'dbconn'):
        flask.g.dbconn = psycopg2.connect(
            database=config.DB_NAME, host=config.DB_HOST,
            user=config.DB_USER, password=config.DB_PASS)
    return flask.g.dbconn

def get_cursor():
    return get_connection().cursor(
        cursor_factory=psycopg2.extras.DictCursor)

def query_one (sql, **params):
    with get_cursor() as cur:
        cur.execute(sql, params)
        res = cur.fetchone()
        if res:
            return dict(res)
        else:
            return {}

def query_all (sql, **params):
    with get_cursor() as cur:
        cur.execute(sql, params)
        result = cur.fetchall()
        res = []
        for row in result:
            res.append(dict(row))
        return res

def insert (sql, **params):
    with get_cursor() as cur:
        cur.execute(sql, params)
        conn = flask.g.dbconn
        conn.commit()

def _rollback_db (sender, exception, **extra):
    if hasattr(flask.g, 'dbconn'):
        conn = flask.g.dbconn
        conn.rollback()
        conn.close()
        delattr(flask.g, 'dbconn')

def _commit_db (sender, exception, **extra):
    if hasattr(flask.g, 'dbconn'):
        conn = flask.g.dbconn
        conn.commit()
        conn.close()


# sudo su - postgres
# pg_dump -s track > 000_schema.sql
# ls back/sql/* | sort | xargs psql track -f


# psql --host=localhost --user=lmironov track
# lmironov