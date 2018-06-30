from API.config import open_connection, close_connection, json, status, re, uuid, hashlib

MIN_LENGTH = 6
MAX_LENGTH = 50

def login_api(request):
    """The Login API checks to see if the user is trying to login with a valid Customer_Number and Password"""

    data = request.data
    json_data = json.loads(data)

    #If test is passed as an input and its true, we set the test flag as true to use the Testing database
    if "test" in json_data:
        test = json_data["test"]
    else:
        test = False

    Customer_Number = json_data["Customer_Number"]
    Password =  json_data["Password"]

    #Validating the input to only process valid data. We return an error if the data is not valid
    valid_input = Validate_Input(json_data["Customer_Number"],json_data["Password"])

    if not valid_input:
        return ('', 400) #bad request

    
    db_context = open_connection(test)
    cur = db_context.cursor()


    cur.execute('SELECT * FROM public."Customers" c WHERE c."Active" = true AND c."Customer_Number" = %s', (Customer_Number,))
    result_set = cur.fetchall()
    
    result = []

    #f the result_set is [], a user with the customer number doesnt exist and we return a 404 error
    if not result_set:
        close_connection(cur, db_context)
        return ('', 404)

    colnames = [desc[0] for desc in cur.description]
    customer = result_set[0]

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
    """This function is responsible to validate the input"""
    
    valid = True
    if len(Customer_Number) > MAX_LENGTH:
        valid = False

    return valid

def check_password(hashed_password, input_password):
    """This function compares the input password against the hashed password stored in the database to check if they match"""
    password, salt = hashed_password.split(':')
    return password == hashlib.sha256(salt.encode() + input_password.encode()).hexdigest()