from flask import Flask, render_template, request, redirect, url_for, flash
from flask import session as login_session
import pyrebase

config = {
  'apiKey': "AIzaSyArzqR6Lf2mjF5p8M0gpsP_aflzb0pon7c",
  'authDomain': "cheeeeeeese-f8077.firebaseapp.com",
  'projectId': "cheeeeeeese-f8077",
  'storageBucket': "cheeeeeeese-f8077.appspot.com",
  'messagingSenderId': "660468371911",
  'appId': "1:660468371911:web:ec873b97fb9807274889e2",
  'measurementId': "G-2MHQ6R155G",
  "databaseURL": ""
};


firebase = pyrebase.initialize_app(config)
auth = firebase.auth()


app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SECRET_KEY'] = 'super-secret-key'


@app.route('/', methods=['GET', 'POST'])
def signin():
    return render_template("signin.html")


@app.route('/signup', methods=['GET', 'POST'])
def signup():
	if request.method == 'POST':
		email = request.form['email']
		password = request.form['password']
		try:
			login_session['user'] = auth.create_user_with_email_and_password(email, password)
			return redirect(url_for('add_tweet'))
		except:
			error = "Authentication failed"
			return render_template("signup.html")
	return render_template("signup.html")


@app.route('/add_tweet', methods=['GET', 'POST'])
def add_tweet():
    return render_template("add_tweet.html")


if __name__ == '__main__':
    app.run(debug=True)