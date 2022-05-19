from datetime import timedelta
import unicodedata,json, requests
from flask import Flask, session, abort, redirect, request, render_template, url_for
from authlib.integrations.flask_client import OAuth
from auth_decorator import login_required
import os



app = Flask(__name__)
app.secret_key = os.getenv('APP_SECRET_KEY')

app.config['SESSION_COOKIE_NAME'] = 'sventa'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=5)

CONF_URL = 'https://accounts.google.com/.well-known/openid-configuration'

oauth = OAuth(app)
google = oauth.register(
    name='google',
    client_id='506150050561-cdeadtrd8sogc0bk1rjdjsgvjcusopkf.apps.googleusercontent.com',
    client_secret='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',
    server_metadata_url=CONF_URL,
    client_kwargs={'scope': 'openid profile email'}
)


@app.route("/login")
def login():
    google = oauth.create_client('google')
    redirect_uri = url_for('callback', _external=True)
    return google.authorize_redirect(redirect_uri)


@app.route("/callback")
def callback():
    token = oauth.google.authorize_access_token()
    user = token.get('userinfo')
    
    
    session['profile'] = google.userinfo()
    session.permanent = True

    if user:
        session['user'] = user 

    return redirect("/dashboard")

    

@app.route("/logout")
def logout():
    for key in list(session.keys()):
        session.pop(key)

    return redirect("/")

@app.route("/")
def index():
    return "logga in <a href='/login'>logga in</a>"

@app.route("/dashboard")
@login_required
def dashboard():
    user = dict(session).get('profile', None)
    email = user['email']
    #return f"Hello, {email} <br><a href='/logout'>logga ut</a>"


    #session['email'] = user['email']
    #session.permanent = True
    info = requests.get('http://localhost:8081/coupon')
    info = unicodedata.normalize('NFKD', info.text).encode('ascii','ignore')
    info = json.loads(info)
    return render_template('dashboard.html', info=info,user=user)
    #return "Dashboard <a href='/logout'>logga ut</a>"


if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0",port=5000)