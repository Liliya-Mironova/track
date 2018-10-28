from flask import Flask

app = Flask(__name__, instance_relative_config=True)

app.config.from_pyfile('config.py') # default config
app.config.from_pyfile('config.py', silent=True) # local config

# from .views import *
from .handlers import *