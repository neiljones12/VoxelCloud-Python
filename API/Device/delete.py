from API.config import open_connection, close_connection, json, status

def delete_device_api(request):
    data = request.data
    json_data = json.loads(data)
    
    Id = json_data['device_id']

    valid_input = Validate_Input(Id)

    if (not valid_input):
        # return HTTP 400. Bad request
        return ('Invalid data, Please check the documentation', 400)

    if "test" in json_data:
        test = json_data["test"]
    else:
        test = False
    
    db_context = open_connection(test)
    cur = db_context.cursor()

    cur.execute('SELECT * FROM public."Devices" WHERE "Id" = %s', (Id,))

    # Fetching the result
    result_set = cur.fetchall()

    if(result_set == []):
        # return HTTP 404. Device not found
        close_connection(cur, db_context)
        return ('', 404)

    # Executing the query
    cur.execute('UPDATE public."Devices" SET "Active" = False WHERE "Id" = %s', (Id,))
    db_context.commit()
    # Closing the databse connection before returning the result
    close_connection(cur, db_context)
    
    # Return the Http 200 status to show a succcess status
    return ('', 200)

def Validate_Input (device_Id):
    valid = True

    # Validating the device_Id parameter by allowing only numbers
    try: 
        int(device_Id)
        
    except ValueError:
        valid = False

    return valid