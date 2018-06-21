from flask import Flask, current_app, abort, request
from config import db_context
import json

app = Flask(__name__)

# Homepage route.
# Displays API documentation by returning a static html.
@app.route('/')
def index():
    return current_app.send_static_file('apiary.apib')

@app.route('/read', methods=['GET'])
def read():
    if not request.json:
        abort(400)
    print (request.json)
    return json.dumps(request.json)