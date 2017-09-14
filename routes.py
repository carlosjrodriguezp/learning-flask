from flask import Flask, render_template, request, session, redirect, url_for
from models import db, User, Place
from forms import SignupForm, LoginForm, AddressForm

app = Flask(__name__)

#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:local@localhost/learningflask'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://skchdpuqwnwgmw:b94cdacd1447b8940b4d6bd6c8a04cf8bd5ce0a04818c7e8544d746f0e0d454a@ec2-54-243-255-57.compute-1.amazonaws.com/deseobooe9n73f'
db.init_app(app)

app.secret_key = "development-key"

@app.route("/")
def index():
	return render_template("index.html")

@app.route("/about")
def about():
	return render_template("about.html")

@app.route("/signup", methods = ['GET','POST'])
def signup():
	if 'email' in session:
		return redirect(url_for('home'))

	form = SignupForm()

	if request.method == 'POST':
		if form.validate() == False:
			return render_template('signup.html', form=form)
		else:
			newuser = User(form.first_name.data, form.last_name.data, form.email.data, form.password.data)
			db.session.add(newuser)
			db.session.commit()

			session['email'] = form.email
			return redirect(url_for('home'))
	elif request.method == 'GET':
		return render_template('signup.html', form=form)

@app.route("/home", methods = ['GET','POST'])
def home():
	if 'email' not in session:
		return redirect(url_for('login'))

	form = AddressForm()
	
	places = []
	my_coordinates = (37.4221, -122.0844)

	if request.method == 'POST':
		if form.validate() == False:
			return render_template("home.html", form=form)
		else:
			address = form.address.data
			p = Place()
			my_coordinates = p.address_to_latlng(address)
			places = p.query(address)

			return render_template("home.html", form=form, my_coordinates=my_coordinates, places=places)

	elif request.method == 'GET':
		return render_template("home.html", form=form, my_coordinates=my_coordinates, places=places)

@app.route("/login", methods = ['GET','POST'])
def login():
	if 'email' in session:
		return redirect(url_for('home'))

	form = LoginForm()

	if request.method == 'POST':
		if form.validate() == False:
			return render_template('login.html', form=form)
		else:
			user = User.query.filter_by(email=form.email.data).first()
			if user is not None and user.check_password(form.password.data):
				session['email'] = form.email.data
				return redirect(url_for('home'))
			else:
				return redirect(url_for('login'))
	elif request.method == 'GET':
		return render_template('login.html', form=form)

@app.route("/logout")
def logout():
	session.pop('email', None)
	return redirect(url_for('index'))

if __name__ == '__main__':
	app.run(debug=True)