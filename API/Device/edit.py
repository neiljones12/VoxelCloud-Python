from API.config import open_connection, close_connection, json, status, re, req, socket, datetime, time

MAX_LENGTH = 15

def edit_device_api(request):
    data = request.data
    json_data = json.loads(data)
    
    Name = json_data['Name']
    Compressor_status = json_data['Compressor_status']
    Fan_status = json_data['Fan_status']
    Temperature = json_data['Temperature']
    Ip_Address = json_data['Ip_Address']
    Serial_Number = json_data['Serial_Number']
    Mac_Address = json_data['Mac_Address']
    Communication_Frequency = json_data['Communication_Frequency']
    Installation_Date = json_data['Installation_Date']
    Write_Frequency = json_data['Write_Frequency']
    Write_Time = json_data['Write_Time']
    Reporting_Url = json_data['Reporting_Url']

    valid_input = Validate_Input(Name, Compressor_status, Fan_status, Temperature, Ip_Address, Serial_Number, Mac_Address, Communication_Frequency, Installation_Date, Write_Frequency, Write_Time, Reporting_Url)

    if (not valid_input):
        # Returning the HTTP code 400. Bad request
        return ('Invalid data, Please check the documentation', 400)
    
    Temperature_alert = '1' if Temperature > 80 else '0'
    Timestamp = str(time.strftime("%m/%d/%Y %H:%M:%S"))

    # Checking to see if the test value is passed to the API, If test is true, the testing database is used
    if "test" in json_data:
        test = json_data["test"]
    else:
        test = False

    db_context = open_connection(test)
    cur = db_context.cursor()

    # Executing the query
    cur.execute('SELECT * FROM public."Devices" WHERE "Mac_Address" = %s AND "Serial_Number" = %s',(Mac_Address, Serial_Number))

    # Fetching the result
    result_set_check = cur.fetchall()
    exists = True
    # Checking to see if the device exists
    if(result_set_check == []):
        exists = False

    if (exists):
        Compressor_status_string = str(Compressor_status)
        Fan_status_string = str(Fan_status)
        Temperature_string = str(Temperature)
        Communication_Frequency_string = str(Communication_Frequency)
        Write_Frequency_string = str(Write_Frequency)
        Write_Time_string = str(Write_Time)
        Active = 'true'
        colnames = [desc[0] for desc in cur.description]        
        device = result_set_check[0]

        # Saving the result as a key, value pair
        result = dict(zip(colnames,device))
        Id = str(result['Id'])

        cur.execute('UPDATE public."Devices" SET "Name"=%s, "Compressor_status"=%s, "Fan_status"=%s, "Temperature_alert"=%s, "Temperature"=%s, "Ip_Address"=%s, "Communication_Frequency"=%s, "Write_Frequency"=%s, "Write_Time"=%s, "Reporting_Url"=%s, "Timestamp"=%s, "Active"=%s Where "Id"= %s', (Name, Compressor_status_string, Fan_status_string, Temperature_alert, Temperature_string, Ip_Address, Communication_Frequency_string, Write_Frequency_string, Write_Time_string, Reporting_Url, Timestamp, Active, Id))
        db_context.commit()
    
         # Closing the databse connection before returning the result
        close_connection(cur, db_context)
        
        # Return the Http 200 status to show a succcess status
        return ('', 200)
    
    close_connection(cur, db_context)
    # Return the Http 404 status to show that the device does not exist
    return ('Device does not exist', 404)

def Validate_Input(Name, Compressor_status, Fan_status, Temperature, Ip_Address, Serial_Number, Mac_Address, Communication_Frequency, Installation_Date, Write_Frequency, Write_Time, Reporting_Url):
    valid = True

    # Validating the Compressor_status parameter by allowing only numbers
    try: 
        Compressor_status_Range = [0, 1]
        int(Compressor_status)

        # checking to see if the value is within the acceptable value list
        if Compressor_status not in Compressor_status_Range:
            valid = False
        
    except ValueError:
        valid = False

    # Validating the Fan_status parameter by allowing only numbers
    try: 
        Fan_status_Range = [0, 1]
        int(Fan_status)

        # checking to see if the value is within the acceptable value list
        if Fan_status not in Fan_status_Range:
            valid = False

    except ValueError:
        valid = False

    # Validating the Temperature parameter by allowing only numbers
    try: 
        int(Temperature)
        
    except ValueError:
        valid = False
    
    # Validating the Communication_Frequency parameter by allowing only numbers
    try: 
        Communication_Frequency_Range = [24, 48]
        int(Communication_Frequency)

        # checking to see if the value is within the acceptable value list
        if Communication_Frequency not in Communication_Frequency_Range:
            valid = False
        
    except ValueError:
        valid = False

    # Validating the Write_Frequency parameter by allowing only numbers
    try: 
        Write_Frequency_Range = [0, 10, 15, 30, 60]
        int(Write_Frequency)

        # checking to see if the value is within the acceptable value list
        if Write_Frequency not in Write_Frequency_Range:
            valid = False
        
    except ValueError:
        valid = False

    # Validating the Write_Time parameter by allowing only numbers
    try: 
        int(Write_Time)

        # checking to see if the value is within the acceptable value list
        if Write_Time not in range(1, 49):
            valid = False
        
    except ValueError:
        valid = False

    # Validating the Reporting_Url
    if (re.search("http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\), ]|(?:%[0-9a-fA-F][0-9a-fA-F]))+", Reporting_Url) == None):
        valid = False

    # Validating the Name
    if (re.search("^[A-Za-z0-9 ]*$", Name) == None):
        valid = False

    if(len(Name) > MAX_LENGTH):
        valid = False

    # Validating the Ip Address
    try:
        socket.inet_aton(Ip_Address)
    except socket.error:
        valid = False

    # Validating the Installation Date
    try:
        datetime.datetime.strptime(Installation_Date, '%m/%d/%Y %H:%M:%S')
    except ValueError:
        valid = False
    
    # Validating the Mac Address
    if (re.search("^[a-fA-F0-9:]{17}|[a-fA-F0-9]{12}$", Mac_Address) == None):
        valid = False
    
    # Validating the Serial parameter by allowing only characters and numbers
    if (re.search("^[A-Za-z0-9]*$", Serial_Number) == None):
        valid = False
    
    # Checking to see if the serial number is under the Maximum limit
    if( len(Serial_Number) > MAX_LENGTH ):
        valid = False

    return valid