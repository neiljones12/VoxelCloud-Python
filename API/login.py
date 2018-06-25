from API.config import open_connection, close_connection, json, status

def login_api(request):
    # Reading the parameters from the body
    data = request.data
    json_data = json.loads(data)
    
    # Saving the parameters as string
    Customer_Number = "'" + json_data["Customer_Number"] + "'"
    Password =  "'" +json_data["Password"]+ "'"

    # Checking to see if the test value is passed to the API, If test is true, the testing database is used
    if "test" in json_data:
        test = json_data["test"]
    else:
        test = False

    # Appending the paramters to the query string
    query = 'SELECT * FROM public."Customers" c WHERE c."Active" = true AND c."Customer_Number" = '+Customer_Number+' AND c."Password" = '+Password
    db_context = open_connection(test)
    cur = db_context.cursor()

    # Executing the query
    cur.execute(query)

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