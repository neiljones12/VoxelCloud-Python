import os
import psycopg2

#import the configuration via enviornment variables
host = os.getenv('HOST')
dbname = os.getenv('dbname')
user = os.getenv('user')
password = os.getenv('password')
conn_string = "host="+host+" dbname="+dbname+" user="+user+" password="+password

#connect to the database
db_context = psycopg2.connect(conn_string)


