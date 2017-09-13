from flask_wtf import Form
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length

class SignupForm(Form):
	first_name = StringField('First name', validators=[DataRequired('Please, enter your first name.')])
	last_name = StringField('Last name', validators=[DataRequired('Please, enter your last name.')])
	email = StringField('email', validators=[DataRequired('Please, enter your email.'), Email('The email provided is not valid.')])
	password = PasswordField('password', validators=[DataRequired('Please, enter your password.'), Length(min=6, message='The password must contain 6 character or more.')])
	submit = SubmitField('Sign up')