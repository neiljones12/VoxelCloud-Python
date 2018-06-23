import unittest
import flask_testing
from flask import request
import requests
import json

url = 'http://127.0.0.1:5000/'

class TestFunctions(unittest.TestCase):
    def test_read(self):
        read_api = url + 'read'

        parameters = {
                    "mac" : "001122334455",
                    "serial": "1",
                    "test": True
                }

        data = requests.get(url = read_api, data = json.dumps(parameters))
        
        expected_output = {"comm_freq": 24, "write_freq": "Seconds", "write_length_time": 20, "demand_resp_code": "Compressor Off (6min)", "demand_resp_time": "", "reporting_url": "https://voxelcloud-demo-python.herokuapp.com", "mac": "001122334455", "serial": "1"}
        
        data = str(data.content,'utf-8')
        check = json.dumps(expected_output)

        self.maxDiff = None
        self.assertEqual(data,check)

if __name__ == '__main__':
    unittest.main()