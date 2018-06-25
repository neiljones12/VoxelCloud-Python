from API.config import open_connection, close_connection, time, json, status

def write_immediate_api(request):
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
    device = result_set[0]
    # Saving the result as a key, value pair
    result = dict(zip(colnames,device))
    device_Id = str(result['Id'])

    query = 'SELECT * FROM public."DeviceEvents" WHERE "DeviceId" = '+device_Id+''
    # Executing the query
    cur.execute(query)

    # Fetching the result
    result_set = cur.fetchall()

    # Checking if a value matching the device id exists in the deviceEvents table
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
        cur.execute('UPDATE public."DeviceEvents" SET "Status_At_Event_Compressor"=%s, "Status_At_Event_Fan"=%s, "Status_After_Event_Compressor"=%s, "Status_After_Event_Fan"=%s, "Restart_Check_Compressor"=%s, "Restart_Check_Fan"=%s, "Timestamp"=%s WHERE "DeviceId" = %s', (status_at_event_comp, status_at_event_fan, status_after_event_comp, status_after_event_fan, restart_chk_comp, restart_chk_fan, Timestamp, device_Id))
    # A value does not exist, so we will run an insert query
    else:
        cur.execute('INSERT INTO public."DeviceEvents" ("DeviceId", "Status_At_Event_Compressor", "Status_At_Event_Fan", "Status_After_Event_Compressor", "Status_After_Event_Fan", "Restart_Check_Compressor", "Restart_Check_Fan", "Timestamp") VALUES (%s, %s, %s, %s, %s, %s, %s, %s)', (device_Id, status_at_event_comp, status_at_event_fan, status_after_event_comp, status_after_event_fan, restart_chk_comp, restart_chk_fan, Timestamp))

    db_context.commit()
    close_connection(cur, db_context)
    return ('', 200)

