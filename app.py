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

# Login API
@app.route('/login', methods=['POST'])
def login():
    # Reading the parameters from the body
    data = request.data
    json_data = json.loads(data)
    
    # Saving the parameters as string
    Customer_Number = "'" + json_data["Customer_Number"] + "'"
    Password =  "'" +json_data["Password"]+ "'"

    # Checking to see if the test value is passed to the API, If test is true, the testing database is used
    if "test" in json_data:
        test = json_data["test"]
    else:
        test = False

    # Appending the paramters to the query string
    query = 'SELECT * FROM public."Customers" c WHERE c."Active" = true AND c."Customer_Number" = '+Customer_Number+' AND c."Password" = '+Password
    db_context = open_connection(test)
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
    customer = result_set[0]

    # Saving the result as a key, value pair
    result = dict(zip(colnames,customer))

    response = {}
    response['Customer_Id'] = result['Id']

    close_connection(cur, db_context)
    # Return the JSON object and the Http 200 status to show a succucc status
    return json.dumps(response),status.HTTP_200_OK

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

    # Checking to see if the test value is passed to the API, If test is true, the testing database is used
    if "test" in json_data:
        test = json_data["test"]
    else:
        test = False

    # Appending the paramters to the query string
    query = 'SELECT * FROM public."Products" WHERE "Mac_Address" = '+mac+' AND "Serial_Number" = '+serial
    db_context = open_connection(test)
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

    if(not test):
        response['time'] = time.strftime("%H:%M:%S") #current time
    
    response['reporting_url'] = result['Reporting_Url'] #url to report to. (If change, update Chip)
    response['mac'] = json_data["mac"]
    response['serial'] = json_data["serial"]
    
    # calculating the delay in milliseconds
    end = int(round(time.time() * 1000))
    if(not test):
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

    # Checking to see if the test value is passed to the API, If test is true, the testing database is used
    if "test" in json_data:
        test = json_data["test"]
    else:
        test = False

    # Appending the paramters to the query string
    query = 'SELECT * FROM public."Products" WHERE "Mac_Address" = '+mac+' AND "Serial_Number" = '+serial
    
    db_context = open_connection(test)
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

    # Checking to see if the test value is passed to the API, If test is true, the testing database is used
    if "test" in json_data:
        test = json_data["test"]
    else:
        test = False

    # Appending the paramters to the query string
    query = 'SELECT * FROM public."Products" WHERE "Mac_Address" = '+mac+' AND "Serial_Number" = '+serial
    
    db_context = open_connection(test)
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

    customer_Id = request.args.get('customer_Id')

    if (customer_Id == None):
        # Reading the parameters from the body
        data = request.data
        print(data)
        json_data = json.loads(data)
        
        # Saving the parameters as string
        customer_Id =  str(json_data["customer_Id"])
    
    # Checking to see if the test value is passed to the API, If test is true, the testing database is used
    if "test" in json_data:
        test = json_data["test"]
    else:
        test = False

    # Opening the connection to the database
    db_context = open_connection(test)
    cur = db_context.cursor()

    query = 'SELECT * FROM public."Customers" c, public."CustomerLocations" cl, public."Locations" l WHERE c."Id" = cl."CustomerId" AND cl."LocationId" = l."Id" And c."Id" = '+customer_Id

    # Executing the query
    cur.execute(query)

    # Fetching the result
    result_set = cur.fetchall()
    result = []

    if(result_set == []):
        # Returning the HTTP code 204 because the server successfully processed the request, but is not returning any content.
        close_connection(cur, db_context)
        return ('', 204)

    colnames = [desc[0] for desc in cur.description]

    result = dict(zip(colnames,result_set[0]))
    response = {}

    response['customer_details'] ={
            'Customer_Number': result['Customer_Number'],
            'Location_Id': result['LocationId'],
            'Location_Name': result['Name']
        }

    query_product_list = 'SELECT * FROM public."Customers" c, public."CustomerProducts" cp, public."Products" p WHERE c."Id" = cp."CustomerId" AND cp."ProductId" = p."Id" AND c."Id" = '+customer_Id

    cur.execute(query_product_list)

    # Fetching the result
    result_set_product_list = cur.fetchall()
    result_product_list = []

    # Checking to see if there are any products associated with the customer
    if(result_set_product_list != []):
        colnames_product_list = [desc[0] for desc in cur.description]

        for row in result_set_product_list:
            result_product_list.append(dict(zip(colnames_product_list, row)))

    response['customer_products'] = []

    for row in result_product_list:
        response['customer_products'].append({
            'Product_Id': row['ProductId'],
            'Product_Name': row['Name']
        })

    close_connection(cur, db_context)
    # Return the JSON object and the Http 200 status to show a succucc status
    return json.dumps(response),status.HTTP_200_OK

# View Product API
@app.route('/view_product', methods=['GET'])
def view_product():
    # Reading the parameters from the body
    data = request.data
    json_data = json.loads(data)
    
    # Saving the parameters as string
    customer_Id =  str(json_data["customer_Id"])
    product_Id =  str(json_data["customer_Id"])
    
    # Checking to see if the test value is passed to the API, If test is true, the testing database is used
    if "test" in json_data:
        test = json_data["test"]
    else:
        test = False

    # Opening the connection to the database
    db_context = open_connection(test)
    cur = db_context.cursor()

    query = 'SELECT * FROM public."CustomerProducts" cp, public."Products" p WHERE cp."ProductId" = p."Id" AND cp."CustomerId" = '+customer_Id+' AND p."Id" ='+product_Id

    # Executing the query
    cur.execute(query)

    # Fetching the result
    result_set = cur.fetchall()
    result = []

    if(result_set == []):
        # Returning the HTTP code 204 because the server successfully processed the request, but is not returning any content.
        close_connection(cur, db_context)
        return ('', 204)

    colnames = [desc[0] for desc in cur.description]

    result = dict(zip(colnames,result_set[0]))
    response = {}

    if test:
        result['Timestamp'] = None

    response['product_details'] ={
            'Product_Id': result['ProductId'],
            'Product_Name': result['Name'],
            'Fan_status': result['Fan_status'],
            'Temperature_alert': result['Temperature_alert'],
            'Temperature': result['Temperature'],
            'Ip_Address': result['Ip_Address'],
            'Serial_Number': result['Serial_Number'],
            'Mac_Address': result['Mac_Address'],
            'Communication_Frequency': result['Communication_Frequency'],
            'Installation_Date': result['Installation_Date'],
            'Write_Frequency': result['Write_Frequency'],
            'Write_Time': result['Write_Time'],
            'Timestamp': result['Timestamp']
        }

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

def open_connection(test):
    #import the configuration via enviornment variables
    host = os.getenv('HOST')
    
    if(test):
        database = 'HVAC_Test'
        dbname = os.getenv('dbname_test')
    else:
        database = 'HVAC'
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
        print('Connected to ',database)
    return db_context

def close_connection(cur, conn):
    print('Disconnected from database')
    cur.close()
    conn.close()