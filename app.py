from flask import Flask, current_app, abort, request
from config import db_context
import json

app = Flask(__name__)

# Homepage route.
# Displays API documentation by returning a static html.
@app.route('/')
def index():
    return current_app.send_static_file('index.html')

@app.route('/read', methods=['GET', 'POST'])
def read():
    data = request.data
    json_data = json.loads(data)
    
    mac = json_data["mac"]
    serial = json_data["serial"]
    
    print("mac: ", mac) 
    print("serial: ", serial) 

    cur = db_context.cursor()
    cur.execute('SELECT * FROM public."Customers"')
    rows = cur.fetchall()
    #print(rows)
    return json.dumps(rows)