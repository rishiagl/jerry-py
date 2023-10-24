import json
from sqlite3 import Cursor
from flask import Blueprint, request
from flask_cors import cross_origin
from marshmallow import Schema, fields

from jerry.db import get_db


class Transaction_metadataSchema(Schema):
    id = fields.Integer()
    company_name = fields.Str()
    type = fields.Str()
    prefix = fields.Str()
    last_inserted_id = fields.Integer()

class Transaction_metadata:
    def __init__(self, id, type, company_name, prefix, last_inserted_id):
        self.id = id
        self.type = type
        self.company_name = company_name
        self.prefix = prefix
        self.last_inserted_id = last_inserted_id

    def __repr__(self):
        return "<Transaction_metadata(type={self.type!r})>".format(self=self)    

bp = Blueprint('transaction_metadata', __name__, url_prefix='/transaction_metadata')

from authlib.integrations.flask_oauth2 import ResourceProtector
from .validator import Auth0JWTBearerTokenValidator

require_auth = ResourceProtector()
validator = Auth0JWTBearerTokenValidator(
    "project-jerry.us.auth0.com",
    "http://127.0.0.1:5000"
)
require_auth.register_token_validator(validator)

def addTransaction_metadata(cursor: Cursor, t: Transaction_metadata):
    cursor.execute(
        'INSERT INTO transaction_metadata(type, company_name, prefix, last_inserted_id) VALUES (?, ?, ?, ?)',
        (t.type, t.company_name, t.prefix, t.last_inserted_id))

def updateTransaction_metadata(cursor: Cursor, t: Transaction_metadata):
    cursor.execute(
        'UPDATE transaction_metadata SET type = ?, company_name = ?, prefix = ?, last_inserted_id = ?) WHERE id = ?',
        (t.type, t.company_name, t.prefix, t.last_inserted_id, t.id))
    
def getTransaction_metadata(cursor: Cursor, type: str, company_name: str) :
    rows = cursor.execute('SELECT * FROM transaction_metadata WHERE type = ? AND company_name = ?', (type, company_name)).fetchall()
    transaction_metadata : Transaction_metadata
    for row in rows:
        transaction_metadata = Transaction_metadata(row[0], row[1], row[2], row[3])
        
    return transaction_metadata
