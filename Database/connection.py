import os
import sys
import psycopg2

# Function to open the database connection
def open_connection(test):
    #import the configuration via enviornment variables
    host = os.getenv('HOST')
    
    if(test):
        database = 'HVAC_Test'
        dbname = os.getenv('dbname_test')
    else:
        database = 'HVAC'
        dbname = os.getenv('dbname')

    user = os.getenv('user')
    password = os.getenv('password')
    conn_string = "host="+host+" dbname="+dbname+" user="+user+" password="+password
    
    #connect to the database
    try:
        db_context = psycopg2.connect(conn_string)
    except psycopg2.OperationalError as e:
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