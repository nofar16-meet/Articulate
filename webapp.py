from flask import Flask, render_template, request, session
app = Flask(__name__, static_url_path="", static_folder="static")
from flask import Flask, render_template, request, redirect,url_for
from flask import session as web_session
from wtforms import *
from flask.ext.wtf import Form
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy.orm import sessionmaker
from flask.ext.bootstrap import Bootstrap
import hashlib
import uuid

app = Flask(__name__)

from database import Base,User
from sqlalchemy import create_engine
engine=create_engine('sqlite:///Webpage.db')
Base.metadata.create_all(engine)
DBSessionMaker=sessionmaker(bind=engine)
DBsession=DBSessionMaker()

app.config['SECRET_KEY'] = 'guess who'

db = SQLAlchemy(app)
bootstrap = Bootstrap(app)
'''
if DBsession.query.all()=null:#no users exist:
	users = [
		{
			firstname: 'asdfasd',

		}
	]

	# for user in users
	insertUser = User(fisrname = user.firstname, las)
	#user1=User(

	DBsession.commit()
'''
@app.route('/')
def entry():
	return render_template('entry.html')


class SignUpForm(Form):
	first_name = StringField("First name:")
	last_name = StringField("Last name:")
	email = StringField("Email:", [validators.Email()])
	password = PasswordField("Password:", [validators.Required()])
	gender = SelectField("Gender:", choices = [("male", "Male"), ("female", "Female"), ("other", "Other")])
	date_of_birth = DateField("Date of birth:", [validators.Required()])
	nationality=StringField("Nationality:")
	biography = TextAreaField("Tell us about yourself")
	profile_pic = FileField("You can upload a profile picture.")

	submit = SubmitField("Submit:")

def hash_password(password):
	return hashlib.md5(password.encode()).hexdigest()

@app.route('/signup', methods=['GET', 'POST'])
def signup():

	signup_form = SignUpForm()
	if request.method == 'GET':
		return render_template('signup.html', form = signup_form)


	else:
		firstname=request.form['first_name']

		lastname=request.form['last_name']
		email=request.form['email']
		password=request.form['password']
		password = hash_password(password)
		gender=request.form['gender']
		nationality=request.form['nationality']
		dob=request.form['date_of_birth']
		biography=request.form['biography']

		#profilepic=request.form['profile_pic']
		#user=User(id= 1,firstname='roni',lastname='var',password='jj', email='hello', gender='male',date='1',bio='hi',username='ron',nationality='polish',profilepic='k')
		user=User(firstname=firstname, lastname=lastname,email=email, password=password, gender=gender, nationality=nationality,date=dob,bio=biography)
		DBsession.add(user)
		DBsession.commit()
		print (user.lastname)
		email=DBsession.query(User).filter_by(email=user.email).first().email
		print (email)
		session['id']=uuid.uuid4()
		return redirect(url_for('home',name=firstname))



class Loginform(Form):
	email=StringField('Email:',[validators.Required()])
	password=PasswordField('Password:',[validators.required()])
	submit=SubmitField('Submit')



@app.route('/login',methods=['GET','POST'])
def login():

	loginform=Loginform()

	def validate(email,password):



		return query.first() != None


	if request.method=='GET':
		return render_template('login.html', form=loginform)
	else:
		email=request.form['email']
		password=request.form['password']

		user_query = DBsession.query(User).filter(User.email.in_([email]), User.password.in_([hash_password(password)]))

		user = user_query.first()
		if user != None:
			session['id']=uuid.uuid4()
			return redirect(url_for('home',name=user.firstname))

		return render_template('login.html',form=loginform)




'''
	loger=DBsession.query(User).filter_by(email=email)
	if DBsession.query(User).filter_by(email=loger.email)!=None:
		if loger.password==DBsession.query(User).filter_by(email=loger.email).password:
			return redirect (url_for('home',name=DBsession.query(User).filter_by(email=loger.email).firstname))
'''

@app.route('/user/<name>')
def profile(name):
	return render_template('profile.html', name = name)

@app.route('/home/user/<name>')
def home(name):
	return render_template('home.html', name=name)

@app.route ('/canvas/user/<name>')
def canvas(name):
	return render_template('canvas.html', name=name)

@app.route ('/chat/user/<name>')
def chat(name):
	return render_template('chat.html')
@app.route ('/about')
def about():
	return render_template('about.html')


if __name__ == '__main__':
	app.run(debug=True)
