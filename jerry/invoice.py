import json, os
from sqlite3 import Cursor
from flask import Blueprint, request
from flask_cors import cross_origin
from marshmallow import Schema, fields
from jerry.transaction_metadata import getTransaction_metadata, updateTransaction_metadata
from datetime import date
from jerry.invoice_product import addInvoiceProduct, InvoiceProduct

from jerry.db import get_db


class InvoiceSchema(Schema):
    id = fields.Integer()
    invoice_no = fields.Str()
    company_name = fields.Str()
    date_created = fields.Str()
    customer_phone_no = fields.Integer()
    taxable_value = fields.Integer()
    cgst = fields.Integer()
    sgst = fields.Integer()
    igst = fields.Integer()
    amount = fields.Integer()
    amount_paid = fields.Integer()
    finance_name = fields.Str()
    finance_duration_in_months = fields.Integer()
    dp = fields.Integer()
    emi = fields.Integer()
    narration = fields.Str()
    is_cancelled = fields.Integer()


class Invoice:
    def __init__(self, id, invoice_no, company_name, date_created, customer_phone_no, taxable_value, cgst, sgst, igst, amount, amount_paid, finance_name, finance_duration_in_months, dp, emi, narration, is_cancelled):
        self.id = id
        self.invoice_no = invoice_no
        self.company_name = company_name
        self.date_created = date_created
        self.customer_phone_no = customer_phone_no
        self.taxable_value = taxable_value
        self.cgst = cgst
        self.sgst = sgst
        self.igst = igst
        self.amount = amount
        self.amount_paid = amount_paid
        self.finance_name = finance_name
        self.finance_duration_in_months = finance_duration_in_months
        self.dp = dp
        self.emi = emi
        self.narration = narration
        self.is_cancelled = is_cancelled

    def __repr__(self):
        return "<Invoice(name={self.name!r})>".format(self=self)
    

bp = Blueprint('invoice', __name__, url_prefix='/invoice')

from authlib.integrations.flask_oauth2 import ResourceProtector
from .validator import Auth0JWTBearerTokenValidator

require_auth = ResourceProtector()
validator = Auth0JWTBearerTokenValidator(
    os.getenv("AUTH0_PROJECT_URL"),
    os.getenv("AUTH0_API_AUDIENCE")
)
require_auth.register_token_validator(validator)

def addInvoice(cur: Cursor, i: Invoice):
    last_inserted_id = 0
    for row in cur.execute(
        'INSERT INTO invoice(invoice_no, company_name, date_created, customer_phone_no, taxable_value, cgst, sgst, igst, amount, amount_paid, finance_name, finance_duration_in_months, dp, emi, narration, is_cancelled) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
        (i.invoice_no, i.company_name, i.date_created, i.customer_phone_no, i.taxable_value, i.cgst, i.sgst, i.igst, i.amount, i.amount_paid, i.finance_name, i.finance_duration_in_months, i.dp, i.emi, i.narration, i.is_cancelled)):
        last_inserted_id = row[0]
    return last_inserted_id

def getOneInvoice(cur: Cursor, invoice_no: str, company_name: str):
    row = cur.execute('SELECT * FROM invoice where invoice_no = ? AND company_name = ?', (invoice_no, company_name)).fetchone()
    return Invoice(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10], row[11], row[12], row[13], row[14], row[15], row[16])

def getAllInvoice(cur: Cursor, company_name: str):
    rows = cur.execute('SELECT * FROM invoice where company_name = ?', (company_name,)).fetchall()
    jsonres = []
    schema = InvoiceSchema()
    for row in rows:
        jsonres.append(schema.dump(Invoice(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10], row[11], row[12], row[13], row[14], row[15], row[16])))
    return json.dumps(jsonres)
    
    
@bp.route('', methods=['POST'])
@cross_origin()
@require_auth(None)
def addOne():
    company = request.json.get('company')
    customer = request.json.get('customer')
    inv = Invoice(0, 0, company.get('name'), str(date.today()), customer.get('phone_no'), request.json.get('taxable_value'), request.json.get('cgst'), request.json.get('sgst'), request.json.get('igst'), request.json.get('amount'), request.json.get('amount_paid'), request.json.get('finance_name'), request.json.get('finance_duration_in_months'), request.json.get('dp'), request.json.get('emi'), request.json.get('narration'), 0)
    cur = get_db().cursor()
    cur.execute('BEGIN')
    tm = getTransaction_metadata(cur, 'invoice', company.get('name'))
    inv_no = tm.last_inserted_id + 1
    tm.last_inserted_id = inv_no
    updateTransaction_metadata(cur, tm) 
    invoice_no = "" + tm.prefix + str(inv_no)
    inv.invoice_no = invoice_no
    invoice_id = addInvoice(cur, inv)
    for item in request.json.get('item_list'):
        product = item.get('product')
        addInvoiceProduct(cur, InvoiceProduct(0, invoice_no, company.get('name'), product.get('id'), item.get('description'), item.get('qty'), item.get('rate')))
    cur.execute('COMMIT')
    return {'invoice_no': invoice_no}

@bp.route('/', methods=['GET'])
@cross_origin()
@require_auth(None)
def addAll():
    cur = get_db().cursor()
    company_name = request.args.get('company_name', default = '*', type = str)
    return getAllInvoice(cur, company_name)