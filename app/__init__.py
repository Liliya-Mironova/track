from flask import Flask, jsonify, url_for #, redirect, session, request
from flask_jsonrpc import JSONRPC
# import boto3
# from instance import config
from authlib.flask.client import OAuth
from loginpass import create_flask_blueprint
from loginpass import VK

app = Flask(__name__, instance_relative_config=True)
jsonrpc = JSONRPC(app, '/api/')

app.config.from_pyfile('config.py') # default config
app.config.from_pyfile('config.py', silent=True) # local config

# s3_session = boto3.session.Session()
# s3_client = s3_session.client(service_name='s3',
#                             endpoint_url=config.S3_ENDPOINT_URL,
#                             aws_access_key_id=config.S3_ACCESS_KEY_ID,
#                             aws_secret_access_key=config.S3_SECRET_ACCESS_KEY)

oauth = OAuth(app)


from .handlers import *