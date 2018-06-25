from API.config import open_connection, close_connection, time, json, status

def view_device_api(request):
    customer_Id = request.args.get('customer_Id')
    device_Id = request.args.get('device_Id')
    test = False
    if (customer_Id == None and device_Id == None):
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

    # Opening the connection to the database
    db_context = open_connection(test)
    cur = db_context.cursor()

    query = 'SELECT * FROM public."CustomerDevices" cp, public."Devices" p WHERE cp."DeviceId" = p."Id" AND cp."CustomerId" = '+customer_Id+' AND p."Id" ='+device_Id

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

    close_connection(cur, db_context)
    # Return the JSON object and the Http 200 status to show a succucc status
    return json.dumps(response),status.HTTP_200_OK
