from API.config import open_connection, close_connection, time, json, status, re

def view_device_api(request):
    """The View Device API returns the current status of the device to load the dashboard"""
    customer_Id = request.args.get('customer_Id')
    device_Id = request.args.get('device_Id')
    test = False
    if not customer_Id and not device_Id:
        # Reading the parameters from the body
        data = request.data
        json_data = json.loads(data)
        
        # Saving the parameters as string
        customer_Id =  str(json_data["customer_Id"])
        device_Id =  str(json_data["device_Id"])
        
        # Checking to see if the test value is passed to the API, If test is true, the testing database is used
        if "test" in json_data:
            test = json_data["test"]
        else:
            test = False

    valid_input = Validate_Input(customer_Id, device_Id)

    if not valid_input:
        # Returning the HTTP code 204 because the server successfully processed the request, but is not returning any content.
        return ('', 204)


    # Opening the connection to the database
    db_context = open_connection(test)
    cur = db_context.cursor()

    # Executing the query
    cur.execute('SELECT * FROM public."CustomerDevices" cp, public."Devices" p WHERE cp."DeviceId" = p."Id" AND cp."CustomerId" = %s AND p."Id" = %s', (customer_Id, device_Id))

    # Fetching the result
    result_set = cur.fetchall()
    result = []

    if not result_set:
        # Returning the HTTP code 204 because the server successfully processed the request, but is not returning any content.
        close_connection(cur, db_context)
        return ('', 204)

    colnames = [desc[0] for desc in cur.description]

    result = dict(zip(colnames,result_set[0]))
    response = {}

    if test:
        result['Timestamp'] = None

    response['Device_details'] ={
            'Device_Id': result['DeviceId'],
            'Device_Name': result['Name'],
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

    # Closing the databse connection before returning the result
    close_connection(cur, db_context)

    # Return the JSON object and the Http 200 status to show a success status
    return json.dumps(response),status.HTTP_200_OK

def Validate_Input (customer_Id, device_Id):
    """This function is responsible to validate the input"""
    valid = True

    # Validating the customer_Id parameter by allowing only numbers
    try: 
        int(customer_Id)
        
    except ValueError:
        valid = False
    
    # Validating the device_Id parameter by allowing only numbers
    try: 
        int(device_Id)
        
    except ValueError:
        valid = False

    return valid