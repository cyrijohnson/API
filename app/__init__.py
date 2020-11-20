from flask import Flask
from werkzeug.utils import cached_property
from flask_cors import CORS

app = Flask('__AskCoonoor__')
CORS(app)
