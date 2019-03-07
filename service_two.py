import os
import re
import requests

from flask import Flask
from flask import request
from flask import render_template
from flask import redirect
from flask import url_for
from flask import jsonify

from models import db,Service_Model

service_name = 'service_two'

app = Flask(service_name)
tenants = {
	'tenant1' : 'amazon',
	'tenant2' : 'others'
}


# Constants, path for database - different for each tenant as well as service
project_dir = os.path.dirname(os.path.abspath(__file__))
database_file_1 = "sqlite:///{}".format(os.path.join(project_dir,"{}_db_{}.db".format(service_name,tenants['tenant1'])))
database_file_2 = "sqlite:///{}".format(os.path.join(project_dir,"{}_db_{}.db".format(service_name,tenants['tenant2'])))


# Configuring all the databases in sql alchemy binds
app.config['SQLALCHEMY_BINDS'] = {
	tenants['tenant1']: database_file_1,
	tenants['tenant2']: database_file_2
}

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db.init_app(app)


@app.before_request
def before_request():
	# Here for test purpose we are using the something like localhost:5000/tenant1 , for 
	# real purpose we can use the request.host to get the tenant

	for key, value in tenants.items():
		if(value in request.url):
			# Dynamically bind the tenant with the sql alchemy binds to the engine
			db.choose_tenant(value)
			break

	# The below is not needed, only used for test purpose since the sqlite database needs to 
	# be created initially
	db.create_all()


@app.route("/<tenant_name>/", methods=["GET","POST"])
def home(tenant_name):
	if request.form:
		service = Service_Model(title=request.form['title'])
		db.session.add(service)
		db.session.commit()
		return redirect('/'+tenant_name+'/')
	services = Service_Model.query.all()
	return render_template("home.html",services=services)

@app.route("/api/<tenant_name>/{}/".format(service_name), methods=["GET"])
def api_view(tenant_name):
	services = [service.serialize_service() for service in Service_Model.query.all()]
	return jsonify(services) 

@app.route("/info/<tenant_name>/", methods=["GET"])
def call_other_service(tenant_name):
	api_url = 'http://0.0.0.0:5000/api/{}/service_one'.format(tenant_name)
	result = requests.get(api_url)
	return render_template("detail.html",result=result.text) 

if __name__ == "__main__":
	app.run(debug=True,host="0.0.0.0",port=3000)

