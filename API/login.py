from API.config import open_connection, close_connection, json, status, re

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

    if (not valid_input):
        # Returning the HTTP code 204 because the server successfully processed the request, but is not returning any content.
        return ('', 204)

    
    db_context = open_connection(test)
    cur = db_context.cursor()

    # Executing the query
    cur.execute('SELECT * FROM public."Customers" c WHERE c."Active" = true AND c."Customer_Number" = %s AND c."Password" = %s',(Customer_Number, Password))

    # Fetching the result
    result_set = cur.fetchall()
    result = []

    # Checking to see if we recieve any data
    if(result_set == []):
        # Returning the HTTP code 204 because the server successfully processed the request, but is not returning any content.
        close_connection(cur, db_context)
        return ('', 204)

    colnames = [desc[0] for desc in cur.description]
    customer = result_set[0]

    # Saving the result as a key, value pair
    result = dict(zip(colnames,customer))

    response = {}
    response['Customer_Id'] = result['Id']

    # Closing the databse connection before returning the result
    close_connection(cur, db_context)

    # Return the JSON object and the Http 200 status to show a success status
    return json.dumps(response),status.HTTP_200_OK

def Validate_Input (Customer_Number, Password):
    valid = True

    # Validating the Customer_Number parameter by allowing only characters and numbers
    if (re.search("^[A-Za-z0-9]*$", Customer_Number) == None):
        valid = False
    
    # Validating the Password parameter by allowing only characters and numbers

    # at least include a digit number,
    # at least a upcase and a lowcase letter
    # at least a special characters
    # Can contain a space

    #condition = "^(?=.*[a-z])(?=.*[0-9])(?=.*[^\w\*]).{" + str(MIN_LENGTH) +"," + str(MAX_LENGTH) + "}$"

    #if (re.search(condition, Password) == None):
    valid = Password_Verification(Password)

    # validating against the maximum input length
    if (len(Customer_Number) > MAX_LENGTH):
        valid = False

    return valid

# Password verification without RegEx
def Password_Verification(Password):

    if(len(Password) > MAX_LENGTH):
        return False
    
    contains_lower = False
    constains_upper = False
    contains_special_character = False

    # Special character definition
    special_characters= "_&@#%^$!"

    # Iterating through the string
    for c in Password:
        if c.isupper():
            constains_upper = True
        if c.islower():
            contains_lower = True
        if c in special_characters:
            contains_special_character = True
        
        print(c)

    # Password is valid it it contains a lowercase character, uppercase character and a special character.
    # All characters are permitted
    if(contains_lower and constains_upper and contains_special_character):
        return True
    else:
        return False