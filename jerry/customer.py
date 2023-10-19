import json
from flask import Blueprint, request
from flask_cors import cross_origin
from marshmallow import Schema, fields

from jerry.db import get_db


class CustomerSchema(Schema):
    id = fields.Integer()
    phone_no = fields.Str()
    name = fields.Str()
    address = fields.Str()


class Customer:
    def __init__(self, id, phone_no, name, address):
        self.id = id
        self.phone_no = phone_no
        self.name = name
        self.address = address

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
        jsonRes.append(schema.dump(Customer(row[0], row[1], row[2], row[3])))
    return json.dumps(jsonRes)

def addCustomer(c: Customer):
    db = get_db().cursor()
    db.execute(
        'INSERT INTO customer(phone_no, name, address) VALUES (?, ?, ?)',
        (c.phone_no, c.name, c.address))
    
    
@bp.route('', methods=['POST'])
@cross_origin()
@require_auth(None)
def addOne():
    id = addCustomer(Customer(0, request.json.get('phone_no'), request.json.get('name'), request.json.get('address')))
    return {}


