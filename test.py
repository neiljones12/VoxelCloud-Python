import unittest
import flask_testing
from flask import request

url = 'https://voxelcloud-demo-python.herokuapp.com/'

class TestFunctions(unittest.TestCase):
    def test_read(self):
        parameters = {
                        "mac" : "001122334455",
                        "serial": "1",
                        "test": "True"
                    }
        response = request.get(url + 'read', parameters = parameters)
        print(response)
        expected_response = {
                        "comm_freq": 24,
                        "write_freq": "Seconds",
                        "write_length_time": 20,
                        "demand_resp_code": "Compressor Off (6min)",
                        "demand_resp_time": "",
                        "time": "12:37:10",
                        "reporting_url": "https://voxelcloud-demo-python.herokuapp.com",
                        "mac": "'001122334455'",
                        "serial": "'1'",
                        "delay": 1432
                    }
        self.assertEqual(response.json(), expected_response)

if __name__ == '__main__':
    unittest.main()