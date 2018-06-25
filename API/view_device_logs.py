from API.config import open_connection, close_connection, time, json, status

def view_device_logs_api(request):
    device_Id = request.args.get('device_Id')
    test = False
    if (device_Id == None):
        # Reading the parameters from the body
        data = request.data
        json_data = json.loads(data)
        
        # Saving the parameters as string
        device_Id =  str(json_data["device_Id"])
        
        # Checking to see if the test value is passed to the API, If test is true, the testing database is used
        if "test" in json_data:
            test = json_data["test"]
        else:
            test = False

    # Opening the connection to the database
    db_context = open_connection(test)
    cur = db_context.cursor() 

    query = 'SELECT * FROM public."DeviceEvents" e WHERE e."DeviceId" ='+device_Id

    if(test):
        query += ' AND e."Id"=1'

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

    for row in result_set:
        result.append(dict(zip(colnames,row)))

    response = []
    
    for data in result:
        if not test:
            timestamp =  data['Timestamp']
        else:
            timestamp = None
            
        response.append({
                'Id': data['Id'],
                'Device_Id': data['DeviceId'],
                'Status_At_Event_Compressor': data['Status_At_Event_Compressor'],
                'Status_At_Event_Fan': data['Status_At_Event_Fan'],
                'Status_After_Event_Compressor': data['Status_After_Event_Compressor'],
                'Status_After_Event_Fan': data['Status_After_Event_Fan'],
                'Restart_Check_Compressor': data['Restart_Check_Compressor'],
                'Restart_Check_Fan': data['Restart_Check_Fan'],
                'Temperature': data['Temperature'],
                'Timestamp':timestamp
        })

    # Closing the databse connection before returning the result
    close_connection(cur, db_context)

    # Return the JSON object and the Http 200 status to show a success status
    return json.dumps(response),status.HTTP_200_OK
