import unittest
import flask_testing
from flask import request
import requests
import json

url = 'http://127.0.0.1:5000/'

class TestFunctions(unittest.TestCase):
    # Testing the Read API with valid inputs
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

    # Testing the Read API with invalid inputs
    def test_read_invalid(self):
        read_api = url + 'read'

        parameters = {
                    "mac" : "00",
                    "serial": "1",
                    "test": True
                }

        data = requests.get(url = read_api, data = json.dumps(parameters))
        expected_output = '<Response [204]>'
        
        self.maxDiff = None
        self.assertEqual(str(data),expected_output)

    # Testing the View API with valid inputs
    def test_view(self):
        read_api = url + 'view'

        parameters = {
                    "customer_Id" : "1",
                    "test": True
                }

        data = requests.get(url = read_api, data = json.dumps(parameters))
        
        expected_output = {
                    "customer_details": {
                        "Customer_Number": "AA1122",
                        "Location_Id": 1,
                        "Location_Name": "Location 1"
                    },
                    "customer_products": [
                        {
                            "Product_Id": 1,
                            "Product_Name": "Product 1"
                        },
                        {
                            "Product_Id": 2,
                            "Product_Name": "Product 2"
                        }
                    ]
                }
        
        data = str(data.content,'utf-8')
        check = json.dumps(expected_output)

        self.maxDiff = None
        self.assertEqual(data,check)


    # Testing the View API with invalid inputs
    def test_view_invalid(self):
        read_api = url + 'view'

        parameters = {
                    "customer_Id" : "0",
                    "test": True
                }
                
        data = requests.get(url = read_api, data = json.dumps(parameters))
        expected_output = '<Response [204]>'
        
        self.maxDiff = None
        self.assertEqual(str(data),expected_output)

    # Testing the view_product API with valid inputs
    def test_view_product(self):
        read_api = url + 'view_product'

        parameters = {
                    "customer_Id" : "1",
	                "product_Id":1,
                    "test": True
                }

        data = requests.get(url = read_api, data = json.dumps(parameters))
        
        expected_output = {
                "product_details": {
                    "Product_Id": 1,
                    "Product_Name": "Product 1",
                    "Fan_status": 0,
                    "Temperature_alert": 0,
                    "Temperature": 80,
                    "Ip_Address": "10.0.0.4",
                    "Serial_Number": "1",
                    "Mac_Address": "001122334455",
                    "Communication_Frequency": 24,
                    "Installation_Date": "6/22/2018",
                    "Write_Frequency": 10,
                    "Write_Time": 20,
                    "Timestamp": None
                }
            }
        
        data = str(data.content,'utf-8')
        check = json.dumps(expected_output)

        self.maxDiff = None
        self.assertEqual(data,check)

    # Testing the view_product API with invalid inputs
    def test_view_product_invalid(self):
        read_api = url + 'view_product'

        parameters = {
                    "customer_Id" : "0",
                    "test": True
                }
                
        data = requests.get(url = read_api, data = json.dumps(parameters))
        expected_output = '<Response [204]>'
        
        self.maxDiff = None
        self.assertEqual(str(data),expected_output)

    # Testing the write API with valid inputs
    def test_write(self):
        read_api = url + 'write'

        parameters = {
                "comp_status": 1,
                "fan_status": 0,
                "temp_alert": 0,
                "temp": 80,
                "mac": "001122334455",
                "serial": "1",
                "test": True
            }
                
        data = requests.put(url = read_api, data = json.dumps(parameters))
        expected_output = '<Response [200]>'
        
        self.maxDiff = None
        self.assertEqual(str(data),expected_output)

        # Testing the write API with invalid inputs
    def test_write_invalid(self):
        read_api = url + 'write'

        parameters = {
                "comp_status": 1,
                "fan_status": 0,
                "temp_alert": 0,
                "temp": 80,
                "mac": "001122334455",
                "serial": "0",
                "test": True
            }
                
        data = requests.put(url = read_api, data = json.dumps(parameters))
        expected_output = '<Response [204]>'
        
        self.maxDiff = None
        self.assertEqual(str(data),expected_output)

    # Testing the write_immediate API with valid inputs
    def test_write_immediate(self):
        read_api = url + 'write_immediate'

        parameters = {
                "status_at_event_comp": "0",
                "status_at_event_fan": "0",
                "status_after_event_comp": "0",
                "status_after_event_fan": "0",
                "restart_chk_comp": "1",
                "restart_chk_fan": "1",
                "mac": "001122334455",
                "serial": "1",
                "test": True
            }
                
        data = requests.put(url = read_api, data = json.dumps(parameters))
        expected_output = '<Response [200]>'
        
        self.maxDiff = None
        self.assertEqual(str(data),expected_output)

        # Testing the write_immediate API with invalid inputs
    def test_write_immediate_invalid(self):
        read_api = url + 'write_immediate'

        parameters = {
                "status_at_event_comp": "0",
                "status_at_event_fan": "0",
                "status_after_event_comp": "0",
                "status_after_event_fan": "0",
                "restart_chk_comp": "1",
                "restart_chk_fan": "1",
                "mac": "001122334455",
                "serial": "0",
                "test": True
            }
                
        data = requests.put(url = read_api, data = json.dumps(parameters))
        expected_output = '<Response [204]>'
        
        self.maxDiff = None
        self.assertEqual(str(data),expected_output)

if __name__ == '__main__':
    unittest.main()