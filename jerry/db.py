import sqlite3, os
import apsw

import click
from flask import current_app, g

def get_db():
    if 'db' not in g:
        g.db = apsw.Connection(os.getenv("SQLITE_DB_DEST"))

    return g.db


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()
    
def init_app(app):
    app.teardown_appcontext(close_db)