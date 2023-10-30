import json, os
from sqlite3 import Cursor
from flask import Blueprint, request
from flask_cors import cross_origin
from marshmallow import Schema, fields
from jerry.company_users import CompanyUsers, addCompanyUser

from jerry.db import get_db
from jerry.transaction_metadata import Transaction_metadata, addTransaction_metadata


class CompanySchema(Schema):
    id = fields.Integer()
    name = fields.Str()
    legal_name = fields.Str()
    address = fields.Str()
    city = fields.Str()
    state = fields.Str()
    pincode = fields.Str()
    gstn = fields.Str()
    phone_no = fields.Str()
    email = fields.Email()
    website = fields.Str()
    bank_name = fields.Str()
    account_no = fields.Str()
    ifsc_code = fields.Str()
    upi_id = fields.Str()
    owner_email = fields.Email()


class Company:
    def __init__(self, id, name, legal_name, address, city, state, pincode, gstn, phone_no, email, website, bank_name, account_no, ifsc_code, upi_id, owner_email):
        self.id = id
        self.name = name
        self.legal_name = legal_name
        self.address = address
        self.city = city
        self.state = state
        self.pincode = pincode
        self.gstn = gstn
        self.phone_no = phone_no
        self.email = email
        self.website = website
        self.bank_name = bank_name
        self.account_no = account_no
        self.ifsc_code = ifsc_code
        self.upi_id = upi_id
        self.owner_email = owner_email

    def __repr__(self):
        return "<Company(name={self.name!r})>".format(self=self)
    

bp = Blueprint('company', __name__, url_prefix='/company')

from authlib.integrations.flask_oauth2 import ResourceProtector
from .validator import Auth0JWTBearerTokenValidator

require_auth = ResourceProtector()
validator = Auth0JWTBearerTokenValidator(
    os.getenv("AUTH0_PROJECT_URL"),
    os.getenv("AUTH0_API_AUDIENCE")
)
require_auth.register_token_validator(validator)

def addCompany(cursor: Cursor, c: Company):
    for row in cursor.execute(
        'INSERT INTO company(name, legal_name, address, gstn, city, state, pincode, phone_no, email, website, bank_name, account_no, ifsc_code, upi_id, owner_email) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?); SELECT last_insert_rowid()',
        (c.name, c.legal_name, c.address, c.city, c.state, c.pincode, c.gstn, c.phone_no, c.email, c.website, c.bank_name, c.account_no, c.ifsc_code, c.upi_id, c.owner_email)):
        last_insert_id = row[0]
    return last_insert_id

def getCompanyByID(cursor: Cursor, id: str):
    row = cursor.execute(
        'SELECT * FROM company where id=?', (id,)
    ).fetchone()
    return Company(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10], row[11], row[12], row[13], row[14], row[15])

def getCompanyByName(cursor: Cursor, company_name: str):
    row = cursor.execute(
        'SELECT * FROM company where name=?', (company_name,)
    ).fetchone()
    return Company(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10], row[11], row[12], row[13], row[14], row[15])
    
@bp.route('', methods=['POST'])
@cross_origin()
@require_auth(None)
def addOne():
    cur = get_db().cursor()
    cur.execute('BEGIN')
    id = addCompany(cur, Company(0, request.json.get('name'), request.json.get('legal_name'), request.json.get('address'), request.json.get('city'), request.json.get('state'), request.json.get('pincode'), request.json.get('gstn'), request.json.get('phone_no'), request.json.get('email'), request.json.get('website'), request.json.get('bank_name'), request.json.get('account_no'), request.json.get('ifsc_code'), request.json.get('upi_id'), request.json.get('owner_email')))
    addCompanyUser(cur, CompanyUsers(0, id, request.json.get('name'), request.json.get('owner_email')))
    addTransaction_metadata(cur, Transaction_metadata(0, 'invoice', request.json.get('name'), 'inv', 0))
    cur.execute('COMMIT')
    return {}

@bp.route('/<id>', methods=['GET'])
@cross_origin()
@require_auth(None)
def getById(id):
    cur = get_db().cursor()
    company = getCompanyByID(cur, id)
    return CompanySchema().dump(company)


