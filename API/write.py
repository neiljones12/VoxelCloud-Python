from API.config import open_connection, close_connection, time, json, status, re

MAX_LENGTH = 15

def write_api(request):
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
    query = 'SELECT * FROM public."Devices" WHERE "Mac_Address" = '+mac+' AND "Serial_Number" = '+serial
    
    valid_input = Validate_Input(json_data["mac"],json_data["serial"])

    if (not valid_input):
        # Returning the HTTP code 204 because the server successfully processed the request, but is not returning any content.
        return ('', 204)


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
    
    # Setting a flag to check if the inputs are valid and within bounds before writing to the database
    valid_input = True

    Compressor_status = str(json_data["comp_status"])

    # Compressor_status can only accept 0 or 1.
    if(int(Compressor_status) < 0 or int(Compressor_status) > 1):
        valid_input = False

    Fan_status = str(json_data["fan_status"])

    # Fan_status can only accept 0 or 1.
    if(int(Fan_status) < 0 or int(Fan_status) > 1):
        valid_input = False

    Temperature_alert = str(json_data["temp_alert"])

    # Temperature_alert can only accept 0 or 1.
    if(int(Temperature_alert) < 0 or int(Temperature_alert) > 1):
        valid_input = False

    Temperature = str(json_data["temp"])
    Timestamp = str(time.strftime("%m/%d/%Y %H:%M:%S"))
    Mac_Address = json_data["mac"]
    Serial_Number = json_data["serial"]

    if (valid_input):
        cur.execute('UPDATE public."Devices" SET "Compressor_status"=%s, "Fan_status"=%s, "Temperature_alert"=%s, "Temperature"=%s, "Timestamp"=%s WHERE "Mac_Address" = %s AND "Serial_Number" = %s', (Compressor_status,Fan_status,Temperature_alert,Temperature,Timestamp,Mac_Address,Serial_Number))
        db_context.commit()

    # Closing the databse connection before returning the result
    close_connection(cur, db_context)

    if (valid_input):
        # Return the Http 200 status to show a succcess status
        return ('', 200)
    else:
        # Return an Http 400 status to show a bad request because of invalid data
        return ('Invalid data, Please check the documentation', 400)

def Validate_Input (Mac, Serial):
    valid = True

    # Validating the Mac Address
    if (re.search("^[a-fA-F0-9:]{17}|[a-fA-F0-9]{12}$", Mac) == None):
        valid = False
    
    # Validating the Serial parameter by allowing only characters and numbers
    if (re.search("^[A-Za-z0-9]*$", Serial) == None):
        valid = False
    
    # Checking to see if the serial number is under the Maximum limit
    if( len(Serial) > MAX_LENGTH ):
        valid = False

    return valid