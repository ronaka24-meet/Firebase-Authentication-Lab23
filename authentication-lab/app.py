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
  "databaseURL": "https://cheeeeeeese-f8077-default-rtdb.europe-west1.firebasedatabase.app/"
};


firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
db = firebase.database()


app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SECRET_KEY'] = 'super-secret-key'


@app.route('/', methods=['GET', 'POST'])
def signin():
	if request.method == 'POST':
		email = request.form['email']
		password = request.form['password']
		try:
			login_session['user'] = auth.sign_in_with_email_and_password(email, password)
			return redirect(url_for('add_tweet'))
		except:
			error = "Authentication failed"
			return render_template("signin.html")
	return render_template("signin.html")


@app.route('/signup', methods=['GET', 'POST'])
def signup():
	if request.method == 'POST':
		email = request.form['email']
		password = request.form['password']
		full_name = request.form['full_name']
		username = request.form['username']
		bio = request.form['bio']
		try:
			login_session['user'] = auth.create_user_with_email_and_password(email, password)
			UID = login_session['user']['localId']
			user = {'email': email, 'password': password, 'full_name': full_name, 'username': username, 'bio': bio}
			db.child("Users").child(UID).set(user)
			return redirect(url_for('add_tweet'))
		except:
			error = "Authentication failed"
			return render_template("signup.html")
	return render_template("signup.html")


@app.route('/add_tweet', methods=['GET', 'POST'])
def add_tweet():
	if request.method == 'POST':
		UID = login_session['user']['localId']
		try:
			tweet = {"title": request.form['title'], "text": request.form['text'], 'uid': UID}
			db.child("tweets").push(tweet)
			return render_template("add_tweet.html")
		except:
			print("Couldn't post")
	return render_template("add_tweet.html")

@app.route('/all_tweets', methods=['GET', 'POST'])
def disply_tweets():
	tweets = db.child("tweets").get().val()
	return render_template("tweets.html", tweets=tweets)


if __name__ == '__main__':
    app.run(debug=True)