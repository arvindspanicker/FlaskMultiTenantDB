import os
import re

from flask import Flask
from flask import request
from flask import render_template
from flask import redirect
from flask import url_for

from multitenant_db_setup import MultiTenantSQLAlchemy


app = Flask(__name__)


# Constants, path for database
project_dir = os.path.dirname(os.path.abspath(__file__))
database_file_1 = "sqlite:///{}".format(os.path.join(project_dir,"service_one_db_1.db"))
database_file_2 = "sqlite:///{}".format(os.path.join(project_dir,"service_one_db_2.db"))


# Configuring all the databases in sql alchemy binds
app.config['SQLALCHEMY_BINDS'] = {
	'tenant1': database_file_1,
	'tenant2': database_file_2
}

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = MultiTenantSQLAlchemy(app)


@app.before_request
def before_request():
	# Here for test purpose we are using the something like localhost:5000/tenant1 , for 
	# real purpose we can use the request.host to get the tenant
	tenant = request.url.replace('http://localhost:','').replace('/','')
	tenant = re.sub("\d", "", tenant)

	# Dynamically bind the tenant with the sql alchemy binds to the engine
	db.choose_tenant(tenant)

	# The below is not needed, only used for test purpose since the sqlite database needs to be created
	db.create_all()


class Service_Model(db.Model):
	__tablename__ = 'services_list'
	title = db.Column(db.String(100), nullable=False,primary_key=True)


@app.route("/<tenant_name>/", methods=["GET","POST"])
def home(tenant_name):
	if request.form:
		service = Service_Model(title=request.form['title'])
		db.session.add(service)
		db.session.commit()
		print('/'+tenant_name+'/')
		return redirect('/'+tenant_name+'/')
	services = Service_Model.query.all()
	return render_template("home.html",services=services)


if __name__ == "__main__":
	app.run(debug=True)

