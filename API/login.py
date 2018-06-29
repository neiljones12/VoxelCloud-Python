from API.config import open_connection, close_connection, json, status, re, uuid, hashlib

MIN_LENGTH = 6
MAX_LENGTH = 50

def login_api(request):
    # Reading the parameters from the body
    data = request.data
    json_data = json.loads(data)
    
    # Saving the parameters as string
    Customer_Number = json_data["Customer_Number"]
    Password =  json_data["Password"]

    # Checking to see if the test value is passed to the API, If test is true, the testing database is used
    if "test" in json_data:
        test = json_data["test"]
    else:
        test = False

    # Passing the parameters into the Validate_Input method to validate them
    valid_input = Validate_Input(json_data["Customer_Number"],json_data["Password"])

    if not valid_input:
        # Returning the HTTP code 204 because the server successfully processed the request, but is not returning any content.
        return ('', 204)

    
    db_context = open_connection(test)
    cur = db_context.cursor()

    # Executing the query
    cur.execute('SELECT * FROM public."Customers" c WHERE c."Active" = true AND c."Customer_Number" = %s', (Customer_Number,))

    # Fetching the result
    result_set = cur.fetchall()
    result = []

    # Checking to see if we recieve any data
    if result_set == []:
        # Returning the HTTP code 404 because a user could not be found.
        close_connection(cur, db_context)
        return ('', 404)

    colnames = [desc[0] for desc in cur.description]
    customer = result_set[0]

    # Saving the result as a key, value pair
    result = dict(zip(colnames,customer))
    response = {}

    password_check = check_password(result['PasswordHash'], Password)
    
    if password_check:
        response['Customer_Id'] = result['Id']

        # Closing the databse connection before returning the result
        close_connection(cur, db_context)

        # Return the JSON object and the Http 200 status to show a success status
        return json.dumps(response),status.HTTP_200_OK
    
    else:
        # Returning the HTTP code 204 because the server successfully processed the request, but is not returning any content.
        return ('', 204)

def Validate_Input (Customer_Number, Password):
    valid = True

    # validating against the maximum input length
    if len(Customer_Number) > MAX_LENGTH:
        valid = False

    return valid

def check_password(hashed_password, input_password):
    password, salt = hashed_password.split(':')
    return password == hashlib.sha256(salt.encode() + input_password.encode()).hexdigest()