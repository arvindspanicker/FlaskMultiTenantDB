from multitenant_db_setup import MultiTenantSQLAlchemy

db = MultiTenantSQLAlchemy()


class Service_Model(db.Model):
	__tablename__ = 'services_list'
	title = db.Column(db.String(100), nullable=False,primary_key=True)

	def serialize_service(self):
		return {"title": self.title}
