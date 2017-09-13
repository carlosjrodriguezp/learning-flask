from flask_sqlalchemy import SQLAlchemy
from werkzeug import generate_password_hash, check_password_hash

db = SQLAlchemy()

class User(db.Model):
	__tablename__ = 'users'
	uid = db.Column(db.Integer, primary_key = True)
	firstname = db.Column(db.String(100))
	lastname = db.Column(db.String(100))
	email = db.Column(db.String(100), unique = True)
	pwdhash = db.Column(db.String(54))

	def __init__(self, firstname, lastname, email, pwdhash):
		self.firstname = firstname.title()
		self.lastname = lastname.title()
		self.email = email.lower()
		self.set_password(pwdhash)

	def set_password(self, pwdhash):
		self.pwdhash = generate_password_hash(pwdhash)

	def check_password(self, pwdhash):
		return check_password_hash(self.pwdhash, pwdhash)

