from flask import Flask
from flask_jsonrpc import JSONRPC
# from authlib.flask.client import OAuth

app = Flask(__name__, instance_relative_config=True)
jsonrpc = JSONRPC(app, '/api/')
# oauth = OAuth(app)

# oauth.register('messenger',
#     client_id=config.APP_ID,
#     client_secret=config.APP_SECRET,
#     request_token_url='https://api.twitter.com/oauth/request_token',
#     access_token_url='https://api.twitter.com/oauth/access_token',
#     authorize_url='https://api.twitter.com/oauth/authenticate',
#     api_base_url='https://api.twitter.com/1.1/'
# )

app.config.from_pyfile('config.py') # default config
app.config.from_pyfile('config.py', silent=True) # local config

# from .views import *
from .handlers import *