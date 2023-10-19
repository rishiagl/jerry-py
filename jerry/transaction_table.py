import json
from sqlite3 import Cursor
from flask import Blueprint, request
from flask_cors import cross_origin
from marshmallow import Schema, fields

from jerry.db import get_db


class Transaction_tableSchema(Schema):
    id = fields.Integer()
    company_name = fields.Str()
    name = fields.Str()
    prefix = fields.Str()
    last_inserted_id = fields.Integer()

class Transaction_table:
    def __init__(self, id, name, company_name, prefix, last_inserted_id):
        self.id = id
        self.name = name
        self.company_name = company_name
        self.prefix = prefix
        self.last_inserted_id = last_inserted_id

    def __repr__(self):
        return "<Transaction_table(name={self.name!r})>".format(self=self)    

bp = Blueprint('transaction_table', __name__, url_prefix='/transaction_table')

from authlib.integrations.flask_oauth2 import ResourceProtector
from .validator import Auth0JWTBearerTokenValidator

require_auth = ResourceProtector()
validator = Auth0JWTBearerTokenValidator(
    "project-jerry.us.auth0.com",
    "http://127.0.0.1:5000"
)
require_auth.register_token_validator(validator)

def addTransaction_table(cursor: Cursor, t: Transaction_table):
    cursor.execute(
        'INSERT INTO transaction_table(name, company_name, prefix, last_inserted_id) VALUES (?, ?, ?, ?)',
        (t.name, t.company_name, t.prefix, t.last_inserted_id))

def updateTransaction_table(cursor: Cursor, t: Transaction_table):
    cursor.execute(
        'UPDATE transaction_table SET name = ?, company_name = ?, prefix = ?, last_inserted_id = ?) WHERE id = ?',
        (t.name, t.company_name, t.prefix, t.last_inserted_id, t.id))
    
def getTransaction_table(cursor: Cursor, name: str, company_name: str) :
    rows = cursor.execute('SELECT * FROM transaction_table WHERE name = ? AND company_name = ?', (name, company_name)).fetchall()
    transaction_table : Transaction_table
    for row in rows:
        transaction_table = Transaction_table(row[0], row[1], row[2], row[3])
        
    return transaction_table
