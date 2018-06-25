from flask import Flask, current_app, request
app = Flask(__name__)

# Importing the API methods which can be found in the API folder
from API.login import login_api
from API.read import read_api
from API.write import write_api
from API.view import view_api
from API.view_device import view_device_api
from API.write_immediate import write_immediate_api


# Homepage route.
# Displays API documentation by returning a static html.
@app.route('/')
def index():
    return current_app.send_static_file('index.html')

####################################
##         API Methods            ##
####################################

# Login API
@app.route('/login', methods=['POST'])
def login():
    return(login_api(request))

# Read API
@app.route('/read', methods=['GET'])
def read():
    return(read_api(request))

@app.route('/write', methods=['PUT'])
def write():
    return(write_api(request))

@app.route('/write_immediate', methods=['PUT'])
def write_immediate():
    return(write_immediate_api(request))

# View API
@app.route('/view', methods=['GET'])
def view():
    return(view_api(request))

# View device API
@app.route('/view_device', methods=['GET'])
def view_device():
    return(view_device_api(request))