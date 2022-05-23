from crypt import methods
from datetime import timedelta
from enum import unique
import unicodedata,json, requests
from wsgiref.util import request_uri
from flask import Flask, session, abort, redirect, request, render_template, url_for
from authlib.integrations.flask_client import OAuth
#from auth_decorator import login_required
import os, secrets, base64, hashlib
from dotenv import load_dotenv
from flask_cors import CORS
from flask_login import (
    LoginManager,
    current_user,
    login_required,
    login_user,
    logout_user,
)

from user import User

load_dotenv('.okta.env')

app = Flask(__name__)
app.config.update({SECRET_KEY: secrets.token_hex(64)})

CORS(app)

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)


#app.secret_key = os.getenv('APP_SECRET_KEY')

#app.config['SESSION_COOKIE_NAME'] = 'sventa'
#app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=5)

#CONF_URL = 'https://accounts.google.com/.well-known/openid-configuration'

#oauth = OAuth(app)
#google = oauth.register(
#    name='google',

#    server_metadata_url=CONF_URL,
#    client_kwargs={'scope': 'openid profile email'}
#)


@app.route("/login")
def login():
    #session['app_state'] = secrets.token_urlsafe(64)
    #session['code_verifier'] = secrets.token_urlsafe(64)

    session['app_state'] = "test"
    session['code_verifier'] = "sauce"

    hashed = hashlib.sha256(session['code_verifier'].encode('ascii')).digest()
    encoded = base64.urlsafe_b64decode(hashed)
    code_challenge = encoded.decode('ascii').strip('=')

    query_params = {'client_id': os.environ['CLIENT_ID'],
                    'redirect_url': "http://localhost:5000/callback",
                    'scope': "openid email, profile",
                    'state': session['app_state'],
                    'code_challenge': code_challenge,
                    'code_challenge_method': 'S256',
                    'response_type': 'code',
                    'response_mode': 'query'}

    request_uri = "{base_url}?{query_params}".format(
        base_url = os.environ['ORG_URL'] + "oauth2/default/v1/authorize",
        query_params = requests.compat.urlencode(query_params)
    )

    return redirect(request_uri)

    #google = oauth.create_client('google')
    #redirect_uri = url_for('callback', _external=True)
    #return google.authorize_redirect(redirect_uri)


@app.route("/callback")
def callback():
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    code = request.args.get("code")
    app_state = request.args.get("state")
    if app_state != session['app_state']:
        return "The app state does not match"
    if not code:
        return "The code was not returned or is not accessible", 403

    query_params = {'grant_type': 'authorization_code',
                    'code': code,
                    'redirect_uri': request.base_url,
                    'code_verifier': session['code_verifier'],
                    }
    query_params = request.compat.urlencode(query_params)
    exchange = requests.post(

        os.environ['ORG_URL'] + "oauth2/default/v1/token",
        headers = headers,
        data = query_params,
        auth = (os.environ['CLIENT_ID'] + os.environ['CLIENT_SECRET']),
    ).json()

    #Get tokens and validate
    if not exchange.get("token_type"):
        return "Unsupported token type. Should be 'Bearer'.",403
    access_token = exchange["access_token"]
    id_token = exchange["id_token"]

    # Authorization flow sucessful, get userinfo and login user
    userinfo_response = requests.get(os.environ['ORG_URL'] + "oauth2/default/v1/userinfo",
                                    headers={'Authorization': f'Bearer {access_token}'}).json()
    
    unique_id = userinfo_response["sub"]
    user_email = userinfo_response["email"]
    user_name = userinfo_response["given_name"]

    user = User(
        id_=unique_id, name=user_name,email=user_email
    )
    
    if not User.get(unique_id):
        User.create(unique_id, user_name, user_email)

    login_user(user)

    return redirect(url_for("/dashboard"))
    #token = oauth.google.authorize_access_token()
    #user = token.get('userinfo')
    
    
    #session['profile'] = google.userinfo()
    #session.permanent = True

    #if user:
    #    session['user'] = user 

    #return redirect("/dashboard")

    

@app.route("/logout")
@login_required
def logout():
    logout_user()

    return redirect("/")

@app.route("/")
def index():
    return "logga in <a href='/login'>logga in</a>"

@app.route("/dashboard", methods=['POST','GET'])
@login_required
def dashboard():



    #if methods == ['POST']:
    #    requests.post('http://localhost:8081/user_coupon')
    #    return "hello"

    #user = dict(session).get('profile', None)
    #email = user['email']
    #return f"Hello, {email} <br><a href='/logout'>logga ut</a>"


    #session['email'] = user['email']
    #session.permanent = True
    info = requests.get(os.getenv('COUPON_API')+'/coupon')
    info = unicodedata.normalize('NFKD', info.text).encode('ascii','ignore')
    info = json.loads(info)
    return render_template('dashboard.html', info=info,user=user)
    


if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0",port=5000)