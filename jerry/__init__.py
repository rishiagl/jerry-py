import logging
import os
import sys

from dotenv import load_dotenv
from flask import Flask

from flask import has_request_context, request
from flask.logging import default_handler
from flask_cors import CORS

class RequestFormatter(logging.Formatter):
    def format(self, record):
        if has_request_context():
            record.url = request.url
            record.remote_addr = request.remote_addr
        else:
            record.url = None
            record.remote_addr = None

        return super().format(record)

formatter = RequestFormatter(
    '[%(asctime)s] %(remote_addr)s requested %(url)s\n'
    '%(levelname)s in %(module)s: %(message)s'
)
default_handler.setFormatter(formatter)


def create_app(test_config=None):
    
    load_dotenv()
    
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, os.getenv("SQLITE_DB_DEST")),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
    app.logger.addHandler(handler)
    app.logger.setLevel(logging.DEBUG)
    
    from . import db
    db.init_app(app)
    
    from . import company
    app.register_blueprint(company.bp)
    
    from . import company_users
    app.register_blueprint(company_users.bp)
    
    from . import customer
    app.register_blueprint(customer.bp)
    
    from . import product
    app.register_blueprint(product.bp)
    
    from . import invoice
    app.register_blueprint(invoice.bp)
    
    from . import pdf_endpoints
    app.register_blueprint(pdf_endpoints.bp)
    
    CORS(app, origins=[os.getenv("CORS_ORIGIN_1"), os.getenv("CORS_ORIGIN_2")])
    return app