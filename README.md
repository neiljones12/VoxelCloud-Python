# HVAC API

This project contains the methods for an API server for an HVAC IOT device.
The project was developed using Python and the flask microframework

The API docmentation can be found here
https://voxelcloud-demo-python.herokuapp.com/

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

Python
```
https://www.howtogeek.com/197947/how-to-install-python-on-windows/
```

### Installation

Run the following command to install the requirements

```
pip install -r requirements.txt
```

### Running the application

Navigate to the root of the application in Command Prompt as an Administrator.
Run the following commands to Set the enviornment variables
```
env\Scripts\activate
set HOST='voxelcloud.postgres.database.azure.com'
set dbname='HVAC'
set dbname_test= 'HVAC_Test'
set user='neil@voxelcloud'
set password='Welc0me!'
```

Run the application with the command
```
flask run
```
### Testing the application

In a new instance of the Command Prompt navigate to the root of the application as an Administrator.
Run the following commands to Set the enviornment variables
```
env\Scripts\activate
set HOST='voxelcloud.postgres.database.azure.com'
set dbname='HVAC'
set dbname_test= 'HVAC_Test'
set user='neil@voxelcloud'
set password='Welc0me!'
```
Run the tests with the command
```
py test.py
```
