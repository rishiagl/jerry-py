import json
from sqlite3 import Cursor
from flask import Blueprint, request, send_file
from flask_cors import cross_origin
from marshmallow import Schema, fields
from jerry.transaction_metadata import getTransaction_metadata, updateTransaction_metadata
from datetime import date
from jerry.invoice_product import addInvoiceProduct, InvoiceProduct
from jerry.invoice import getOneInvoice, Invoice, InvoiceSchema
from jerry.company import Company, getCompanyByName
from jerry.customer import Customer, getCustomerByPhoneNo
from jerry.invoice_product import InvoiceProduct, getInvoiceProducts
from jerry.pdf.invoice_pdf import invoicePdf
from jerry.product import Product, getProductByID
from jerry.db import get_db

bp = Blueprint('pdf', __name__, url_prefix='/pdf')

from authlib.integrations.flask_oauth2 import ResourceProtector
from .validator import Auth0JWTBearerTokenValidator

require_auth = ResourceProtector()
validator = Auth0JWTBearerTokenValidator(
    "project-jerry.us.auth0.com",
    "http://127.0.0.1:5000"
)
require_auth.register_token_validator(validator)

class Item:
    def __init__(self, product: Product, invoiceProduct: InvoiceProduct):
        self.product = product
        self.invoiceProduct = invoiceProduct
        
@bp.route('/invoice', methods=['POST'])
@cross_origin()
@require_auth(None)
def getInvoicePdf():
    invoice_no = request.json.get('invoice_no')
    company_name = request.json.get('company_name')
    cur = get_db().cursor()
    invoice: Invoice = getOneInvoice(cur, invoice_no, company_name)
    company: Company = getCompanyByName(cur, company_name)
    customer: Customer = getCustomerByPhoneNo(cur, invoice.customer_phone_no)
    invoiceProducts = getInvoiceProducts(cur, company_name, invoice_no)
    itemList = []
    for invoiceProduct in invoiceProducts:
        itemList.append(Item(getProductByID(cur, invoiceProduct.product_id), invoiceProduct))
    buffer = invoicePdf(invoice, company, customer, itemList)
    filename = company_name + "_" + invoice_no + ".pdf"
    return send_file(buffer, download_name=filename)
