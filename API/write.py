from API.config import open_connection, close_connection, time, json, status

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

    #update_query = 'UPDATE public."Devices" SET "Compressor_status"='+Compressor_status+', "Fan_status"='+Fan_status+', "Temperature_alert"='+Temperature_alert+', "Temperature"='+Temperature+', "Timestamp"='+Timestamp+' WHERE "Mac_Address" = '+mac+' AND "Serial_Number" = '+serial

    cur.execute('UPDATE public."Devices" SET "Compressor_status"=%s, "Fan_status"=%s, "Temperature_alert"=%s, "Temperature"=%s, "Timestamp"=%s WHERE "Mac_Address" = %s AND "Serial_Number" = %s', (Compressor_status,Fan_status,Temperature_alert,Temperature,Timestamp,Mac_Address,Serial_Number))
    db_context.commit()
    #cur.execute(update_query)

    close_connection(cur, db_context)
    return ('', 200)

