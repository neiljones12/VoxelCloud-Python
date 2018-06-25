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

    Timestamp = str(time.strftime("%H:%M:%S"))

    if(valid_input):
        # A value exists, so we will run an update query
        if(isExist):
            cur.execute('UPDATE public."DeviceEvents" SET "Status_At_Event_Compressor"=%s, "Status_At_Event_Fan"=%s, "Status_After_Event_Compressor"=%s, "Status_After_Event_Fan"=%s, "Restart_Check_Compressor"=%s, "Restart_Check_Fan"=%s, "Timestamp"=%s WHERE "DeviceId" = %s', (status_at_event_comp, status_at_event_fan, status_after_event_comp, status_after_event_fan, restart_chk_comp, restart_chk_fan, Timestamp, device_Id))
        # A value does not exist, so we will run an insert query
        else:
            cur.execute('INSERT INTO public."DeviceEvents" ("DeviceId", "Status_At_Event_Compressor", "Status_At_Event_Fan", "Status_After_Event_Compressor", "Status_After_Event_Fan", "Restart_Check_Compressor", "Restart_Check_Fan", "Timestamp") VALUES (%s, %s, %s, %s, %s, %s, %s, %s)', (device_Id, status_at_event_comp, status_at_event_fan, status_after_event_comp, status_after_event_fan, restart_chk_comp, restart_chk_fan, Timestamp))

        db_context.commit()

    # Closing the databse connection before returning the result
    close_connection(cur, db_context)
    
    if (valid_input):
        # Return the Http 200 status to show a succcess status
        return ('', 200)
    else:
        # Return an Http 400 status to show a bad request because of invalid data
        return ('Invalid data, Please check the documentation', 400)

