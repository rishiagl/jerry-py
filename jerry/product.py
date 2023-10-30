import json, os
from sqlite3 import Cursor
from flask import Blueprint, request
from flask_cors import cross_origin
from marshmallow import Schema, fields

from jerry.db import get_db


class ProductSchema(Schema):
    id = fields.Integer()
    name = fields.Str()
    hsn = fields.Str()
    tax_rate = fields.Integer()


class Product:
    def __init__(self, id, name, hsn, tax_rate):
        self.id = id
        self.name = name
        self.hsn = hsn
        self.tax_rate = tax_rate

    def __repr__(self):
        return "<Product(name={self.name!r})>".format(self=self)
    

bp = Blueprint('product', __name__, url_prefix='/product')

from authlib.integrations.flask_oauth2 import ResourceProtector
from .validator import Auth0JWTBearerTokenValidator

require_auth = ResourceProtector()
validator = Auth0JWTBearerTokenValidator(
    os.getenv("AUTH0_PROJECT_URL"),
    os.getenv("AUTH0_API_AUDIENCE")
)
require_auth.register_token_validator(validator)

def getProductByID(cur: Cursor, id: int):
    row = cur.execute('SELECT * FROM product where id=?', (id,)).fetchone()
    return Product(row[0], row[1], row[2], row[3])

@bp.route('', methods=['GET'])
@cross_origin()
@require_auth(None)
def getAll():
    db = get_db().cursor()
    rows = db.execute(
        'SELECT * FROM product'
    ).fetchall()
    jsonRes = []
    schema = ProductSchema()
    for row in rows:
        jsonRes.append(schema.dump(Product(row[0], row[1], row[2], row[3])))
    return json.dumps(jsonRes)


def addProduct(cur: Cursor, c: Product):
    for row in cur.execute(
        'INSERT INTO product(name, hsn, tax_rate) VALUES (?, ?, ?)',
        (c.name, c.hsn, c.tax_rate)):
        last_inserted_row_id = row[0]
    return last_inserted_row_id
    
    
@bp.route('', methods=['POST'])
@cross_origin()
@require_auth(None)
def addOne():
    cur = get_db().cursor()
    id = addProduct(cur, Product(0, request.json.get('name'), request.json.get('hsn'), request.json.get('tax_rate')))
    return {}
