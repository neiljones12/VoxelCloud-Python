from flask import Flask
import os

import psycopg2

host = os.getenv('HOST')
dbname = os.getenv('dbname')
user = os.getenv('user')
password = os.getenv('password')


conn_string = "host="+host+" dbname="+dbname+" user="+user+" password="+password
conn = psycopg2.connect(conn_string)

app = Flask(__name__)

@app.route("/")
def index():
    cur = conn.cursor()
    cur.execute('SELECT * FROM public."Customers"')
    rows = cur.fetchall()
    print(rows)

    return "<h1>TEST<h1>"


if __name__ == '__main__':
    app.run(debug=True)