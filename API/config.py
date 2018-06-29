import time
import json
from flask_api import status
import re
import socket
import urllib.request as req
import datetime
from flask import Flask, current_app, abort, request

# Importing the functions responsible for the database connection
from Database.connection import open_connection, close_connection

### Below are the helper methods

# Function to return the compressor status
def conpressor_status_display(status):
    result = ''
    if (status == 0):
        result = 'No event'
    elif (status == 1):
        result = 'Compressor Off (6min)'
    elif (status == 2):
        result = 'Compressor Off (12min)'
    elif (status == 3):
        result = 'Comp&Fan Off (12min)'
        
    return result

# function to return the write frequency status
def write_freq_display(status):
    result = ''
    if (status == 0):
        result = 'No write'
    elif (status == 10):
        result = 'Seconds'
    elif (status == 15 or status == 30 or status == 60):
        result = 'Seconds power sampling / reporting'

    return result