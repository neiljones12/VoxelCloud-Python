from flask import Flask, current_app, abort, request
from flask_api import status
from config import db_context
import time
import json

app = Flask(__name__)

# Homepage route.
# Displays API documentation by returning a static html.
@app.route('/')
def index():
    return current_app.send_static_file('index.html')

# Read API
@app.route('/read', methods=['GET'])
def read():
    start = int(round(time.time() * 1000))
    # Reading the parameters from the body
    data = request.data
    json_data = json.loads(data)
    
    # Saving the parameters as string
    mac = "'" + json_data["mac"] + "'"
    serial =  "'" +json_data["serial"]+ "'"

    # Appending the paramters to the query string
    query = 'SELECT * FROM public."Products" WHERE "MacAddress" = '+mac+' AND "SerialNumber" = '+serial
    cur = db_context.cursor()

    # Executing the query
    cur.execute(query)

    # Fetching the result
    result_set = cur.fetchall()
    result = []

    # Checking to see if we recieve any data
    if(result_set == []):
        # Returning the HTTP code 204 because the server successfully processed the request, but is not returning any content.
        return ('', 204)

    colnames = [desc[0] for desc in cur.description]
    product = result_set[0]

    # Saving the result as a key, value pair
    result = dict(zip(colnames,product))

    response = {}
    response['comm_freq'] = result['Communication_Frequency']

    # Passing the value of the Write_Frequency to the write_freq_display function in order to display the appropriate message
    response['write_freq'] = write_freq_display(result['Write_Frequency'])
    response['write_length_time'] = result['Write_Time']

    # Passing the value of the Compressor_status to the conpressor_status_display function in order to display the appropriate message
    response['demand_resp_code'] =  conpressor_status_display(result['Compressor_status']) #0=No event /1=Compressor Off (6min)/2=Compressor Off (12min)/ 3=Comp&Fan Off (12min)
    response['demand_resp_time'] = '' #time H:M:S
    response['time'] = time.strftime("%H:%M:%S") #current time
    
    response['reporting_url'] = result['Reporting_Url'] #url to report to. (If change, update Chip)
    response['mac'] = mac
    response['serial'] = serial
    
    # calculating the delay in milliseconds
    end = int(round(time.time() * 1000))
    response['delay'] = end - start #Delay in milli-seconds after the event.

    # Return the JSON object and the Http 200 status to show a succucc status
    return json.dumps(response),status.HTTP_200_OK


@app.route('/write', methods=['PUT'])
def write():
    data = request.data
    json_data = json.loads(data)
    
    # Saving the parameters as string
    mac = "'" + json_data["mac"] + "'"
    serial =  "'" +json_data["serial"]+ "'"

    # Appending the paramters to the query string
    query = 'SELECT * FROM public."Products" WHERE "MacAddress" = '+mac+' AND "SerialNumber" = '+serial
    cur = db_context.cursor()

    # Executing the query
    cur.execute(query)

    # Fetching the result
    result_set = cur.fetchall()

    if (result_set == []):
        # Returning the HTTP code 204 because the server successfully processed the request, but is not returning any content.
        return ('', 204)
    
    Compressor_status = str(json_data["comp_status"])
    Fan_status = str(json_data["fan_status"])
    Temperature_alert = str(json_data["temp_alert"])
    Temperature = str(json_data["temp"])

    update_query = 'UPDATE public."Products" SET "Compressor_status"='+Compressor_status+', "Fan_status"='+Fan_status+', "Temperature_alert"='+Temperature_alert+', "Temperature"='+Temperature+' WHERE "MacAddress" = '+mac+' AND "SerialNumber" = '+serial

    cur.execute(update_query)

    # Return HTTP status code 400 Bad Request for an unsuccessful PUT
    if(cur.rowcount != 1):
        abort(400)
    
    return ('', 200)

# Function to return the compressor status
def conpressor_status_display(status):
    result = ''
    if (status == 0):
        result = 'No event'
    elif (status == 1):
        result = 'Compressor Off (6min)'
    elif (status == 2):
        result = 'Compressor Off (12min)'
    elif (status == 3):
        result = 'Comp&Fan Off (12min)'
        
    return result

# function to return the write frequency status
def write_freq_display(status):
    result = ''
    if (status == 0):
        result = 'No write'
    elif (status == 10):
        result = 'Seconds'
    elif (status == 15 or status == 30 or status == 60):
        result = 'Seconds power sampling / reporting'

    return result