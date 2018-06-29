import time
import json
from flask_api import status
import re
import socket
import urllib.request as req
import datetime
from flask import current_app, abort, request
import uuid
import hashlib
from Database.connection import open_connection, close_connection

def conpressor_status_display(status):
    """ A helper function to interpret the compressor status"""
    result = ''
    if status == 0:
        result = 'No event'
    elif status == 1:
        result = 'Compressor Off (6min)'
    elif status == 2:
        result = 'Compressor Off (12min)'
    elif status == 3:
        result = 'Comp&Fan Off (12min)'
        
    return result

def write_freq_display(status):
    """A helper function to interpret the write frequency"""
    result = ''
    if status == 0:
        result = 'No write'
    elif status == 10:
        result = 'Seconds'
    elif status == 15 or status == 30 or status == 60:
        result = 'Seconds power sampling / reporting'

    return result