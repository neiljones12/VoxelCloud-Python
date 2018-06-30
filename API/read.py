from API.config import open_connection, close_connection, write_freq_display, conpressor_status_display, time, json, status, re, MAX_LENGTH

def read_api(request):
    """The Read API returns the current status of a device"""

    # Starting a timer
    start = int(round(time.time() * 1000))
    
    # Reading the parameters from the body
    data = request.data
    json_data = json.loads(data)
    
    mac = json_data["mac"]
    serial =  json_data["serial"]

    valid_input = Validate_Input(json_data["mac"],json_data["serial"])

    if not valid_input:
        # Returning the HTTP code 204 because the server successfully processed the request, but is not returning any content.
        return ('', 204)

    # Checking to see if the test value is passed to the API, If test is true, the testing database is used
    if "test" in json_data:
        test = json_data["test"]
    else:
        test = False

    # Appending the paramters to the query string
    db_context = open_connection(test)
    cur = db_context.cursor()

    # Executing the query
    # pyscopg2 will sanitize your query
    cur.execute('SELECT * FROM public."Devices" WHERE "Mac_Address" = %s AND "Serial_Number" = %s', (str(mac), str(serial)))

    # Fetching the result
    result_set = cur.fetchall()
    result = []

    # Checking to see if we recieve any data
    if not result_set:
        # Returning the HTTP code 204 because the server successfully processed the request, but is not returning any content.
        close_connection(cur, db_context)
        return ('', 204)

    colnames = [desc[0] for desc in cur.description]
    device = result_set[0]

    # Saving the result as a key, value pair
    result = dict(zip(colnames,device))

    response = {}
    response['comm_freq'] = result['Communication_Frequency']

    # Passing the value of the Write_Frequency to the write_freq_display function in order to display the appropriate message
    response['write_freq'] = write_freq_display(result['Write_Frequency'])
    response['write_length_time'] = result['Write_Time']

    # Passing the value of the Compressor_status to the conpressor_status_display function in order to display the appropriate message
    response['demand_resp_code'] =  conpressor_status_display(result['Compressor_status']) #0=No event /1=Compressor Off (6min)/2=Compressor Off (12min)/ 3=Comp&Fan Off (12min)
    response['demand_resp_time'] = '' #time H:M:S

    if not test:
        response['time'] = time.strftime("%H:%M:%S") #current time
    
    response['reporting_url'] = result['Reporting_Url'] #url to report to. (If change, update Chip)
    response['mac'] = json_data["mac"]
    response['serial'] = json_data["serial"]
    
    # calculating the delay in milliseconds
    end = int(round(time.time() * 1000))
    if not test:
        response['delay'] = end - start #Delay in milli-seconds after the event.
    
    # Closing the databse connection before returning the result
    close_connection(cur, db_context)

    # Return the JSON object and the Http 200 status to show a success status
    return json.dumps(response),status.HTTP_200_OK

def Validate_Input (Mac, Serial):
    """This function is responsible to validate the input"""
    valid = True

    # Validating the Mac Address
    if re.search("^[a-fA-F0-9:]{17}|[a-fA-F0-9]{12}$", Mac) == None:
        valid = False
    
    if len(Serial) > MAX_LENGTH:
        valid = False

    return valid