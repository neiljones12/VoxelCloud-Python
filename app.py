from flask import Flask, current_app, request
app = Flask(__name__)

# Importing the API methods which can be found in the API folder
from API.login import login_api
from API.read import read_api
from API.write import write_api
from API.view import view_api
from API.view_device import view_device_api
from API.view_device_logs import view_device_logs_api
from API.write_immediate import write_immediate_api
from API.Device.add import add_device_api
from API.Device.delete import delete_device_api
from API.Device.edit import edit_device_api

@app.route('/')
def index():
    """Homepage route. Displays API documentation by returning index.html which can be found in the static folder."""
    return current_app.send_static_file('index.html')


@app.route('/login', methods=['POST'])
def login():
    """Login route. The customer_id is returned on success."""
    return(login_api(request))

@app.route('/read', methods=['GET'])
def read():
    """Read route. Reads the current status of a device."""
    return(read_api(request))

@app.route('/write', methods=['PUT'])
def write():
    """Write route. writes the current status of a device."""
    return(write_api(request))

@app.route('/write_immediate', methods=['PUT'])
def write_immediate():
    """Write_immediate route. logs the current status of a device."""
    return(write_immediate_api(request))

@app.route('/view', methods=['GET'])
def view():
    """View route. Returns data to load the dashboard."""
    return(view_api(request))

@app.route('/view_device', methods=['GET'])
def view_device():
    """View_device route. Returns device information."""
    return(view_device_api(request))

@app.route('/view_device_logs', methods=['GET'])
def view_device_logs():
    """View_device_logs route. Returns device logs."""
    return(view_device_logs_api(request))

@app.route('/add_device', methods=['POST'])
def add_device():
    """Add_device route. Adds a new device."""
    return(add_device_api(request))

@app.route('/delete_device', methods=['DELETE'])
def delete_device():
    """Delete_device route. Deletes a device."""
    return(delete_device_api(request))

@app.route('/edit_device', methods=['PUT'])
def edit_device():
    """Edit_device route. Updates a device."""
    return(edit_device_api(request))
