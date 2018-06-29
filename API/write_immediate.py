from API.config import open_connection, close_connection, time, json, status, re

MAX_LENGTH = 15

def write_immediate_api(request):
    """The Write Immidiate API is used to log each transaction to the database"""
    data = request.data
    json_data = json.loads(data)
    
    # Saving the parameters as string
    mac = json_data["mac"]
    serial = json_data["serial"]

    # Checking to see if the test value is passed to the API, If test is true, the testing database is used
    if "test" in json_data:
        test = json_data["test"]
    else:
        test = False

    valid_input = Validate_Input(json_data["mac"],json_data["serial"])

    if (not valid_input):
        # Returning the HTTP code 204 because the server successfully processed the request, but is not returning any content.
        return ('', 204)

    # Appending the paramters to the query string
    db_context = open_connection(test)
    cur = db_context.cursor()

    # Executing the query
    cur.execute('SELECT * FROM public."Devices" WHERE "Mac_Address" = %s AND "Serial_Number" = %s', (mac, serial))

    # Fetching the result
    result_set = cur.fetchall()
    if (result_set == []):
        # Returning the HTTP code 204 because the server successfully processed the request, but is not returning any content.
        close_connection(cur, db_context)
        return ('', 204)
    
    colnames = [desc[0] for desc in cur.description]
    device = result_set[0]
    # Saving the result as a key, value pair
    result = dict(zip(colnames,device))
    device_Id = str(result['Id'])

    valid_input = True

    status_at_event_comp = str(json_data["status_at_event_comp"])

    # status_at_event_comp can only accept 0 or 1.
    if(int(status_at_event_comp) < 0 or int(status_at_event_comp) > 1):
        valid_input = False

    status_at_event_fan = str(json_data["status_at_event_fan"])

    # status_at_event_fan can only accept 0 or 1.
    if(int(status_at_event_fan) < 0 or int(status_at_event_fan) > 1):
        valid_input = False

    status_after_event_comp = str(json_data["status_after_event_comp"])

    # status_after_event_comp can only accept 0 or 1.
    if(int(status_after_event_comp) < 0 or int(status_after_event_comp) > 1):
        valid_input = False

    status_after_event_fan = str(json_data["status_after_event_fan"])

    # status_after_event_fan can only accept 0 or 1.
    if(int(status_after_event_fan) < 0 or int(status_after_event_fan) > 1):
        valid_input = False

    restart_chk_comp = str(json_data["restart_chk_comp"])

    # restart_chk_comp can only accept 0 or 1.
    if(int(restart_chk_comp) < 0 or int(restart_chk_comp) > 1):
        valid_input = False

    restart_chk_fan = str(json_data["restart_chk_fan"])

    # restart_chk_fan can only accept 0 or 1.
    if(int(restart_chk_fan) < 0 or int(restart_chk_fan) > 1):
        valid_input = False

    Timestamp = str(time.strftime("%m/%d/%Y %H:%M:%S"))

    if valid_input:
        cur.execute('INSERT INTO public."DeviceEvents" ("DeviceId", "Status_At_Event_Compressor", "Status_At_Event_Fan", "Status_After_Event_Compressor", "Status_After_Event_Fan", "Restart_Check_Compressor", "Restart_Check_Fan", "Timestamp") VALUES (%s, %s, %s, %s, %s, %s, %s, %s)', (device_Id, status_at_event_comp, status_at_event_fan, status_after_event_comp, status_after_event_fan, restart_chk_comp, restart_chk_fan, Timestamp))
        db_context.commit()

    # Closing the databse connection before returning the result
    close_connection(cur, db_context)
    
    if valid_input:
        # Return the Http 200 status to show a succcess status
        return ('', 200)
    else:
        # Return an Http 400 status to show a bad request because of invalid data
        return ('Invalid data, Please check the documentation', 400)


def Validate_Input (Mac, Serial):
    """This function is responsible to validate the input"""
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