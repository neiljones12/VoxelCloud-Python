import os
import sys
import psycopg2

# Function to open the database connection
def open_connection(test):

    #import the configuration via enviornment variables
    host = os.getenv('HOST')
    user = os.getenv('user')
    password = os.getenv('password')

    # checking to see if we need to use the testing database or the production database    
    if(test):
        database = 'HVAC_Test'
        dbname = os.getenv('dbname_test')
    else:
        database = 'HVAC'
        dbname = os.getenv('dbname')

    # Building the connection string
    conn_string = "host="+host+" dbname="+dbname+" user="+user+" password="+password
    
    # Trying to establish a databse connection
    try:
        db_context = psycopg2.connect(conn_string)
        
    except psycopg2.OperationalError as e:
        # If an exception is caught, something went wrong while trying to connect
        print('Unable to connect to HVAC!\n{0}').format(e)
        sys.exit(1)
        
    else:
        print('Connected to ',database)
    return db_context

# Function to close the databse connection
def close_connection(cur, conn):
    print('Disconnected from database')
    cur.close()
    conn.close()