import json, os
from sqlite3 import Cursor
from flask import Blueprint, request
from flask_cors import cross_origin
from marshmallow import Schema, fields

from jerry.db import get_db


class InvoiceProductSchema(Schema):
    id = fields.Integer()
    company_name = fields.Str()
    invoice_no  = fields.Str()
    product_id = fields.Integer()
    description = fields.Str()
    qty = fields.Integer()
    rate = fields.Integer()

class InvoiceProduct:
    def __init__(self, id, invoice_no, company_name, product_id, description, qty, rate):
        self.id = id
        self.invoice_no = invoice_no
        self.company_name = company_name
        self.product_id = product_id
        self.description = description
        self.qty = qty
        self.rate = rate

    def __repr__(self):
        return "<InvoiceProduct(name={self.name!r})>".format(self=self)
    

bp = Blueprint('invoiceproduct', __name__, url_prefix='/invoiceproduct')

from authlib.integrations.flask_oauth2 import ResourceProtector
from .validator import Auth0JWTBearerTokenValidator

require_auth = ResourceProtector()
validator = Auth0JWTBearerTokenValidator(
    os.getenv("AUTH0_PROJECT_URL"),
    os.getenv("AUTH0_API_AUDIENCE")
)
require_auth.register_token_validator(validator)

def addInvoiceProduct(cur: Cursor, c: InvoiceProduct):
    last_inserted_id = 0
    for row in cur.execute(
        'INSERT INTO invoice_product(company_name, invoice_no, product_id, description, qty, rate) VALUES (?, ?, ?, ?, ?, ?)',
        (c.company_name, c.invoice_no, c.product_id, c.description, c.qty, c.rate)):
        last_inserted_id = row[0]
    return last_inserted_id

def getInvoiceProducts(cur:Cursor, company_name: str, invoice_no: int):
    InvoiceProducts = []
    for row in cur.execute('SELECT * FROM invoice_product WHERE company_name = ? AND invoice_no = ?', (company_name, invoice_no)):
        InvoiceProducts.append(InvoiceProduct(row[0], row[1], row[2], row[3], row[4], row[5], row[6]))
        
    return InvoiceProducts
    
    

