from API.config import open_connection, close_connection, time, json, status

def view_api(request):
    customer_Id = request.args.get('customer_Id')
    test = False
    if (customer_Id == None):
        # Reading the parameters from the body
        data = request.data
        json_data = json.loads(data)
        
        # Saving the parameters as string
        customer_Id =  str(json_data["customer_Id"])
    
        # Checking to see if the test value is passed to the API, If test is true, the testing database is used
        if "test" in json_data:
            test = json_data["test"]
        else:
            test = False

    # Opening the connection to the database
    db_context = open_connection(test)
    cur = db_context.cursor()

    query = 'SELECT * FROM public."Customers" c, public."CustomerLocations" cl, public."Locations" l WHERE c."Id" = cl."CustomerId" AND cl."LocationId" = l."Id" And c."Id" = '+customer_Id

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

    response['customer_details'] ={
            'Customer_Number': result['Customer_Number'],
            'Location_Id': result['LocationId'],
            'Location_Name': result['Name']
        }

    query_device_list = 'SELECT * FROM public."Customers" c, public."CustomerDevices" cp, public."Devices" p WHERE c."Id" = cp."CustomerId" AND cp."DeviceId" = p."Id" AND c."Id" = '+customer_Id

    cur.execute(query_device_list)

    # Fetching the result
    result_set_device_list = cur.fetchall()
    result_device_list = []

    # Checking to see if there are any devices associated with the customer
    if(result_set_device_list != []):
        colnames_device_list = [desc[0] for desc in cur.description]

        for row in result_set_device_list:
            result_device_list.append(dict(zip(colnames_device_list, row)))

    response['customer_devices'] = []

    for row in result_device_list:
        response['customer_devices'].append({
            'Device_Id': row['DeviceId'],
            'Device_Name': row['Name']
        })

    close_connection(cur, db_context)
    # Return the JSON object and the Http 200 status to show a succucc status
    return json.dumps(response),status.HTTP_200_OK
