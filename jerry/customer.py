import json
from sqlite3 import Cursor
from flask import Blueprint, request
from flask_cors import cross_origin
from marshmallow import Schema, fields

from jerry.db import get_db


class CustomerSchema(Schema):
    phone_no = fields.Str()
    name = fields.Str()
    address = fields.Str()
    state = fields.Str()
    pincode = fields.Str()


class Customer:
    def __init__(self, phone_no, name, address, state, pincode):
        self.phone_no = phone_no
        self.name = name
        self.address = address
        self.state = state
        self.pincode = pincode

    def __repr__(self):
        return "<Customer(name={self.name!r})>".format(self=self)
    

bp = Blueprint('customer', __name__, url_prefix='/customer')

from authlib.integrations.flask_oauth2 import ResourceProtector
from .validator import Auth0JWTBearerTokenValidator

require_auth = ResourceProtector()
validator = Auth0JWTBearerTokenValidator(
    "project-jerry.us.auth0.com",
    "http://127.0.0.1:5000"
)
require_auth.register_token_validator(validator)

def addCustomer(cur: Cursor, c: Customer):
    for row in cur.execute(
        'INSERT INTO customer(phone_no, name, address, state, pincode) VALUES (?, ?, ?, ?, ?)',
        (c.phone_no, c.name, c.address, c.state, c.pincode)):
        
        last_inserted_id = row[0]
    return last_inserted_id

def getCustomerByPhoneNo(cur: Cursor, phone_no: str):
    row = cur.execute('SELECT * FROM customer where phone_no = ?', {phone_no}).fetchone()
    return Customer(row[0], row[1], row[2], row[3], row[4])

@bp.route('', methods=['GET'])
@require_auth(None)
def getAll():
    db = get_db().cursor()
    rows = db.execute(
        'SELECT * FROM customer'
    ).fetchall()
    jsonRes = []
    schema = CustomerSchema()
    for row in rows:
        jsonRes.append(schema.dump(Customer(row[0], row[1], row[2], row[3], row[4])))
    return json.dumps(jsonRes)
    
    
@bp.route('', methods=['POST'])
@cross_origin()
@require_auth(None)
def addOne():
    cur = get_db().cursor()
    id = addCustomer(cur, Customer(request.json.get('phone_no'), request.json.get('name'), request.json.get('address'), request.json.get('state'), request.json.get('pincode')))
    return {}


