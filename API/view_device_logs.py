from API.config import open_connection, close_connection, time, json, status
import datetime

def view_device_logs_api(request):
    # Reading the parameters from the argument
    device_Id = request.args.get('device_Id')
    from_date = request.args.get('from_date')
    to_date = request.args.get('to_date')
    test = False
    if (device_Id == None):
        # Reading the parameters from the body
        data = request.data
        json_data = json.loads(data)
        
        # Saving the parameters as string
        device_Id =  str(json_data["device_Id"])
        
        if from_date in json_data:
            from_date =  str(json_data["from_date"])
        
        if to_date in json_data:
            to_date =  str(json_data["to_date"])
        
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
        add_to_result = True

        # Checking to see if it is the testing enviornment
        if not test:
            timestamp =  data['Timestamp']
            if(from_date and to_date):
                from_date_parse = from_date.split('-') # YYYY MM DD
                to_date_parse = to_date.split('-') # YYYY MM DD
                
                date_parse = timestamp.split('/')
                date_parse[2] = date_parse[2].split(' ')[0] # MM DD YYYY

                # If the date lies inbetween the from and to date, TRUE is returned
                add_to_result = date_check(from_date_parse, to_date_parse, date_parse)
        else:
            timestamp = None

        # If true, the data is added to the response object
        if add_to_result:
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

def date_check(from_date, to_date, date):
    # parsing through the string to seperate the Year, month and day
    from_date_year = int(from_date[0])
    from_date_month = int(from_date[1])
    from_date_day = int(from_date[2])

    to_date_year = int(to_date[0])
    to_date_month = int(to_date[1])
    to_date_day = int(to_date[2])

    date_year = int(date[2])
    date_month = int(date[0])
    date_day = int(date[1])

    # Converting into the datetime object
    from_date = datetime.date(from_date_year, from_date_month, from_date_day)
    to_date = datetime.date(to_date_year, to_date_month, to_date_day)
    current_date = datetime.date(date_year, date_month, date_day)

    # checking to see if the current date is in between the from and to date
    if(to_date >= current_date and current_date >= from_date):
        return True
    else:
        return False