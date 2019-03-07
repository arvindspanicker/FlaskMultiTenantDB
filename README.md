# FlaskMultiTenantDB

Installation
* Create a virtual environment with python3 
* pip install requirments

Running
* Activate the virtual environment
* python app.py


Running on:
* For service-one
 - http://0.0.0.0:5000/amazon 
 - http://0.0.0.0:5000/others

* For service-two
 - http://0.0.0.0:3000/amazon 
 - http://0.0.0.0:3000/others

API Test Among two services
* To test api calls between two of them, first enter data into respective services and tenants db.
* Then http://0.0.0.0:5000/info/amazon/ - will call the service_two which is running on port 3000 and gets the tenant amazon details 
* Similarly http://0.0.0.0:3000/info/amazon/ - will call the service_one which is running on port 5000 and gets the tenant amazon details
