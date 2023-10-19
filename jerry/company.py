import json
from sqlite3 import Cursor
from flask import Blueprint, request
from flask_cors import cross_origin
from marshmallow import Schema, fields
from jerry.company_users import CompanyUsers, addCompanyUser

from jerry.db import get_db
from jerry.transaction_table import Transaction_table, addTransaction_table


class CompanySchema(Schema):
    id = fields.Integer()
    name = fields.Str()
    legal_name = fields.Str()
    address = fields.Str()
    gstn = fields.Str()
    phone_no = fields.Str()
    email = fields.Email()
    website = fields.Str()
    owner_email = fields.Email()


class Company:
    def __init__(self, id, name, legal_name, address, gstn, phone_no, email, website, owner_email):
        self.id = id
        self.name = name
        self.legal_name = legal_name
        self.address = address
        self.gstn = gstn
        self.phone_no = phone_no
        self.email = email
        self.website = website
        self.owner_email = owner_email

    def __repr__(self):
        return "<Company(name={self.name!r})>".format(self=self)
    

bp = Blueprint('company', __name__, url_prefix='/company')

from authlib.integrations.flask_oauth2 import ResourceProtector
from .validator import Auth0JWTBearerTokenValidator

require_auth = ResourceProtector()
validator = Auth0JWTBearerTokenValidator(
    "project-jerry.us.auth0.com",
    "http://127.0.0.1:5000"
)
require_auth.register_token_validator(validator)

def addCompany(cursor: Cursor, c: Company):
    for row in cursor.execute(
        'INSERT INTO company(name, legal_name, address, gstn, phone_no, email, website, owner_email) VALUES (?, ?, ?, ?, ?, ?, ?, ?); SELECT last_insert_rowid()',
        (c.name, c.legal_name, c.address, c.gstn, c.phone_no, c.email, c.website, c.owner_email)):
        last_insert_id = row[0]
    return last_insert_id
    
    
@bp.route('', methods=['POST'])
@cross_origin()
@require_auth(None)
def addOne():
    cur = get_db().cursor()
    cur.execute('BEGIN')
    id = addCompany(cur, Company(0, request.json.get('name'), request.json.get('legal_name'), request.json.get('address'), request.json.get('gstn'), request.json.get('phone_no'), request.json.get('email'), request.json.get('website'), request.json.get('owner_email')))
    addCompanyUser(cur, CompanyUsers(0, id, request.json.get('name'), request.json.get('owner_email')))
    addTransaction_table(cur, Transaction_table(0, 'invoice', request.json.get('name'), 'inv', 0))
    cur.execute('COMMIT')
    return {}

@bp.route('/<id>', methods=['GET'])
@cross_origin()
@require_auth(None)
def getById(id):
    db = get_db().cursor()
    rows = db.execute(
        'SELECT * FROM company where id=?', (id,)
    ).fetchall()
    jsonRes = {}
    schema = CompanySchema()
    for row in rows:
        jsonRes = schema.dump(Company(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8]))
    return json.dumps(jsonRes)


