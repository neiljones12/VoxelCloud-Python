from flask import Flask, current_app, abort, request
from flask_api import status
import time
import json
import os
import sys
import psycopg2

app = Flask(__name__)

# Homepage route.
# Displays API documentation by returning a static html.
@app.route('/')
def index():
    return current_app.send_static_file('index.html')

####################################
##         API Methods            ##
####################################

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
    query = 'SELECT * FROM public."Products" WHERE "Mac_Address" = '+mac+' AND "Serial_Number" = '+serial
    db_context = open_connection()
    cur = db_context.cursor()

    # Executing the query
    cur.execute(query)

    # Fetching the result
    result_set = cur.fetchall()
    result = []

    # Checking to see if we recieve any data
    if(result_set == []):
        # Returning the HTTP code 204 because the server successfully processed the request, but is not returning any content.
        close_connection(cur, db_context)
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
    
    close_connection(cur, db_context)
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
    query = 'SELECT * FROM public."Products" WHERE "Mac_Address" = '+mac+' AND "Serial_Number" = '+serial
    
    db_context = open_connection()
    cur = db_context.cursor()

    # Executing the query
    cur.execute(query)

    # Fetching the result
    result_set = cur.fetchall()

    if (result_set == []):
        # Returning the HTTP code 204 because the server successfully processed the request, but is not returning any content.
        close_connection(cur, db_context)
        return ('', 204)
    
    Compressor_status = str(json_data["comp_status"])
    Fan_status = str(json_data["fan_status"])
    Temperature_alert = str(json_data["temp_alert"])
    Temperature = str(json_data["temp"])
    Timestamp = str(time.strftime("%H:%M:%S"))
    Mac_Address = json_data["mac"]
    Serial_Number = json_data["serial"]

    #update_query = 'UPDATE public."Products" SET "Compressor_status"='+Compressor_status+', "Fan_status"='+Fan_status+', "Temperature_alert"='+Temperature_alert+', "Temperature"='+Temperature+', "Timestamp"='+Timestamp+' WHERE "Mac_Address" = '+mac+' AND "Serial_Number" = '+serial

    cur.execute('UPDATE public."Products" SET "Compressor_status"=%s, "Fan_status"=%s, "Temperature_alert"=%s, "Temperature"=%s, "Timestamp"=%s WHERE "Mac_Address" = %s AND "Serial_Number" = %s', (Compressor_status,Fan_status,Temperature_alert,Temperature,Timestamp,Mac_Address,Serial_Number))
    db_context.commit()
    #cur.execute(update_query)

    close_connection(cur, db_context)
    return ('', 200)


@app.route('/write_immediate', methods=['PUT'])
def write_immediate():
    data = request.data
    json_data = json.loads(data)
    
    # Saving the parameters as string
    mac = "'" + json_data["mac"] + "'"
    serial =  "'" +json_data["serial"]+ "'"

    # Appending the paramters to the query string
    query = 'SELECT * FROM public."Products" WHERE "Mac_Address" = '+mac+' AND "Serial_Number" = '+serial
    
    db_context = open_connection()
    cur = db_context.cursor()

    # Executing the query
    cur.execute(query)

    # Fetching the result
    result_set = cur.fetchall()

    if (result_set == []):
        # Returning the HTTP code 204 because the server successfully processed the request, but is not returning any content.
        close_connection(cur, db_context)
        return ('', 204)
    
    colnames = [desc[0] for desc in cur.description]
    product = result_set[0]
    # Saving the result as a key, value pair
    result = dict(zip(colnames,product))
    Product_Id = str(result['Id'])

    query = 'SELECT * FROM public."ProductEvents" WHERE "ProductId" = '+Product_Id+''
    # Executing the query
    cur.execute(query)

    # Fetching the result
    result_set = cur.fetchall()

    # Checking if a value matching the product id exists in the ProductEvents table
    # Modeling the query to insert or update based on the value of the isExist flag
    isExist = True
    if (result_set == []):
        isExist = False

    status_at_event_comp = str(json_data["status_at_event_comp"])
    status_at_event_fan = str(json_data["status_at_event_fan"])
    status_after_event_comp = str(json_data["status_after_event_comp"])
    status_after_event_fan = str(json_data["status_after_event_fan"])
    restart_chk_comp = str(json_data["restart_chk_comp"])
    restart_chk_fan = str(json_data["restart_chk_fan"])
    Timestamp = str(time.strftime("%H:%M:%S"))

    
    # A value exists, so we will run an update query
    if(isExist):
        cur.execute('UPDATE public."ProductEvents" SET "Status_At_Event_Compressor"=%s, "Status_At_Event_Fan"=%s, "Status_After_Event_Compressor"=%s, "Status_After_Event_Fan"=%s, "Restart_Check_Compressor"=%s, "Restart_Check_Fan"=%s, "Timestamp"=%s WHERE "ProductId" = %s', (status_at_event_comp, status_at_event_fan, status_after_event_comp, status_after_event_fan, restart_chk_comp, restart_chk_fan, Timestamp, Product_Id))
    # A value does not exist, so we will run an insert query
    else:
        cur.execute('INSERT INTO public."ProductEvents" ("ProductId", "Status_At_Event_Compressor", "Status_At_Event_Fan", "Status_After_Event_Compressor", "Status_After_Event_Fan", "Restart_Check_Compressor", "Restart_Check_Fan", "Timestamp") VALUES (%s, %s, %s, %s, %s, %s, %s, %s)', (Product_Id, status_at_event_comp, status_at_event_fan, status_after_event_comp, status_after_event_fan, restart_chk_comp, restart_chk_fan, Timestamp))

    db_context.commit()
    close_connection(cur, db_context)
    return ('', 200)


# View API
@app.route('/view', methods=['GET'])
def view():
    start = int(round(time.time() * 1000))
    # Reading the parameters from the body
    data = request.data
    json_data = json.loads(data)
    
    # Saving the parameters as string
    mac = "'" + json_data["mac"] + "'"
    serial =  "'" +json_data["serial"]+ "'"
    customer_Id =  "'" +json_data["customer_Id"]+ "'"

    # Appending the paramters to the query string
    query = 'SELECT * FROM public."Products" WHERE "Mac_Address" = '+mac+' AND "Serial_Number" = '+ serial
    db_context = open_connection()
    cur = db_context.cursor()

    # Executing the query
    cur.execute(query)

    # Fetching the result
    result_set = cur.fetchall()
    result = []

    # Checking to see if we recieve any data
    if(result_set == []):
        # Returning the HTTP code 204 because the server successfully processed the request, but is not returning any content.
        close_connection(cur, db_context)
        return ('', 204)

    colnames = [desc[0] for desc in cur.description]
    product = result_set[0]

    # Saving the result as a key, value pair
    result = dict(zip(colnames,product))

    response = {}
    response['Ip_Address'] = result['Ip_Address']
    response['Mac_Address'] = result['Mac_Address']
    response['Serial_Number'] = result['Serial_Number']
    response['Timestamp'] = result['Timestamp']
    response['Communication_Frequency'] = result['Communication_Frequency']
    
    
    close_connection(cur, db_context)
    # Return the JSON object and the Http 200 status to show a succucc status
    return json.dumps(response),status.HTTP_200_OK




####################################
## Below are the Helper Functions ##
####################################

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

def open_connection():
    #import the configuration via enviornment variables
    host = os.getenv('HOST')
    dbname = os.getenv('dbname')
    user = os.getenv('user')
    password = os.getenv('password')
    conn_string = "host="+host+" dbname="+dbname+" user="+user+" password="+password

    #connect to the database

    try:
        db_context = psycopg2.connect(conn_string)
    except psycopg2.OperationalError as e:
        print('Unable to connect to HVAC!\n{0}').format(e)
        sys.exit(1)
    else:
        print('Connected to HVAC!')
    return db_context

def close_connection(cur, conn):
    print('Disconnected to HVAC!')
    cur.close()
    conn.close()