from flask import Flask, current_app
from config import db_context

app = Flask(__name__)

# Index route.
# Displays API documentation by returning a static html.
@app.route('/')
def index():
    return current_app.send_static_file('index.html')