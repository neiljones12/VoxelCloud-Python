import unittest
import flask_testing
from flask import request
import requests
import json

url = 'http://127.0.0.1:5000/'

class TestFunctions(unittest.TestCase):
    
    # Testing the Login API with valid inputs
    def test_login(self):
        login_api = url + 'login'

        parameters = {
                "Customer_Number": "AA1122",
                "Password": "password",
                "test":True
            }

        data = requests.post(url = login_api, data = json.dumps(parameters))
        
        expected_output = {
                        "Customer_Id": 1
                    }
        
        data = str(data.content,'utf-8')
        check = json.dumps(expected_output)

        self.maxDiff = None
        self.assertEqual(data,check)

    # Testing the Login API with invalid inputs
    def test_login_invalid(self):
        login_api = url + 'login'

        # SQL Injection
        parameters = {
                "Customer_Number": "AA1122",
                "Password": "' or '1'='1",
                "test":True
            }

        data = requests.post(url = login_api, data = json.dumps(parameters))
        expected_output = '<Response [204]>'
        
        self.maxDiff = None
        self.assertEqual(str(data),expected_output)

    # Testing the Login API with invalid inputs (SQL Injection)
    def test_login_invalid_SQL(self):
        login_api = url + 'login'

        parameters = {
                "Customer_Number": "AA1122",
                "Password": "password OR 1=1",
                "test":True
            }

        data = requests.post(url = login_api, data = json.dumps(parameters))
        expected_output = '<Response [204]>'
        
        self.maxDiff = None
        self.assertEqual(str(data),expected_output)
    
    # Testing the Read API with valid inputs
    def test_read(self):
        read_api = url + 'read'

        parameters = {
                    "mac" : "001122334455",
                    "serial": "1001",
                    "test": True
                }

        data = requests.get(url = read_api, data = json.dumps(parameters))
        
        expected_output = {"comm_freq": 24, "write_freq": "Seconds", "write_length_time": 20, "demand_resp_code": "Compressor Off (6min)", "demand_resp_time": "", "reporting_url": "https://voxelcloud-demo-python.herokuapp.com", "mac": "001122334455", "serial": "1001"}
        
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
                    "customer_devices": [
                        {
                            "Device_Id": 1,
                            "Device_Name": "Device 1"
                        },
                        {
                            "Device_Id": 2,
                            "Device_Name": "Device 2"
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

    # Testing the view_device API with valid inputs
    def test_view_device(self):
        read_api = url + 'view_device'

        parameters = {
                    "customer_Id" : "1",
	                "device_Id": "1",
                    "test": True
                }

        data = requests.get(url = read_api, data = json.dumps(parameters))
        
        expected_output = {
                "Device_details": {
                    "Device_Id": 1,
                    "Device_Name": "Device 1",
                    "Fan_status": 0,
                    "Temperature_alert": 0,
                    "Temperature": 75,
                    "Ip_Address": "10.0.0.4",
                    "Serial_Number": "1001",
                    "Mac_Address": "001122334455",
                    "Communication_Frequency": 24,
                    "Installation_Date": "2/25/2017 01:02:03",
                    "Write_Frequency": 10,
                    "Write_Time": 20,
                    "Timestamp": None
                }
            }
        
        data = str(data.content,'utf-8')
        check = json.dumps(expected_output)

        self.maxDiff = None
        self.assertEqual(data,check)

    # Testing the view_device API with invalid inputs
    def test_view_device_invalid(self):
        read_api = url + 'view_device'

        parameters = {
                    "customer_Id" : "0",
	                "device_Id": "1",
                    "test": True
                }
                
        data = requests.get(url = read_api, data = json.dumps(parameters))
        expected_output = '<Response [204]>'
        
        self.maxDiff = None
        self.assertEqual(str(data),expected_output)

     # Testing the view_device_logs API with valid inputs
    def test_view_device_logs(self):
        read_api = url + 'view_device_logs'

        parameters = {
	                "device_Id": "1",
                    "test": True
                }

        data = requests.get(url = read_api, data = json.dumps(parameters))
        
        expected_output = [
                {
                    "Id": 1,
                    "Device_Id": 1,
                    "Status_At_Event_Compressor": 1,
                    "Status_At_Event_Fan": 0,
                    "Status_After_Event_Compressor": 0,
                    "Status_After_Event_Fan": 1,
                    "Restart_Check_Compressor": 0,
                    "Restart_Check_Fan": 0,
                    "Temperature": 75,
                    "Timestamp": None
                }
            ]
        
        data = str(data.content,'utf-8')
        check = json.dumps(expected_output)

        self.maxDiff = None
        self.assertEqual(data,check)
    
    # Testing the view_device_logs API with invalid inputs
    def test_view_device_logs_invalid(self):
        read_api = url + 'view_device_logs'

        parameters = {
	                "device_Id": "0",
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
                "mac": "001122334466",
                "serial": "1002",
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
                "mac": "001122334466",
                "Temperature": "80",
                "serial": "1002",
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
                "serial": "0000",
                "test": True
            }
                
        data = requests.put(url = read_api, data = json.dumps(parameters))
        expected_output = '<Response [204]>'
        
        self.maxDiff = None
        self.assertEqual(str(data),expected_output)

if __name__ == '__main__':
    unittest.main()