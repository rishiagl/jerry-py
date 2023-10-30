from sqlite3 import Cursor
from flask import Blueprint, jsonify, request, g
from flask_cors import cross_origin
from marshmallow import Schema, fields

from jerry.db import get_db
import json, os


import logging

log = logging.getLogger('Manual Log')

class CompanyUsersSchema(Schema):
    id = fields.Integer()
    company_id = fields.Integer()
    company_name = fields.Str()
    user_email = fields.Email()


class CompanyUsers:
    def __init__(self, id, company_id, company_name, user_email):
        self.id = id
        self.company_id = company_id
        self.company_name = company_name
        self.user_email = user_email
    

bp = Blueprint('company-users', __name__, url_prefix='/company-users')

from authlib.integrations.flask_oauth2 import ResourceProtector
from .validator import Auth0JWTBearerTokenValidator

require_auth = ResourceProtector()
validator = Auth0JWTBearerTokenValidator(
    os.getenv("AUTH0_PROJECT_URL"),
    os.getenv("AUTH0_API_AUDIENCE")
)
require_auth.register_token_validator(validator)


import logging
logging.basicConfig(filename='api.log',level=logging.DEBUG)


def addCompanyUser(cur: Cursor, cu: CompanyUsers):
    cur.execute(
        'INSERT INTO company_users(company_id, company_name, user_email) VALUES (?, ?, ?)',
        (cu.company_id, cu.company_name, cu.user_email))

@bp.route('/byEmail', methods=['GET'])
@cross_origin()
@require_auth(None)
def getByEmail():
    db = get_db().cursor()
    rows = db.execute(
        'SELECT * FROM company_users where user_email=?', (request.args.get('user_email'),)
    ).fetchall()
    jsonRes = []
    schema = CompanyUsersSchema()
    for row in rows:
        jsonRes.append(schema.dump(CompanyUsers(row[0], row[1], row[2], row[3])))
    return json.dumps(jsonRes)


@bp.route('', methods=['POST'])
@cross_origin()
@require_auth(None)
def addOne():
    cur = get_db().cursor()
    addCompanyUser(cur, CompanyUsers(0, request.json.get('company_id'), request.json.get('company_name'), request.json.get('user_email')))
    return {}
                   
    
            
            

