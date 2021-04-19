from flask import Flask
from werkzeug.utils import cached_property
from flask_cors import CORS

# Author - Cyril Johnson
# Replace flask server with WGSI for production
# Flask App Initialization & CORS Enablement for local development
app = Flask('__AskCoonoor__')
CORS(app)
