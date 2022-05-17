import requests,unicodedata,json
from flask import Flask, session, abort, redirect, request, render_template
from google_auth_oauthlib.flow import Flow
from google.oauth2 import id_token
import os, pathlib
import google.auth.transport.requests
from pip._vendor import cachecontrol


app = Flask(__name__)
#app.secret_key = os.getenv('APP_SECRET_KEY')
app.secret_key = "test.nu"

# remove sauce
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

GOOGLE_CLIENT_ID = os.getenv('GOOGLE_CLIENT_ID')
client_secrets_file = os.path.join(pathlib.Path(__file__).parent, "client_secrets.json")

flow = Flow.from_client_secrets_file(
    client_secrets_file=client_secrets_file,
    scopes=["https://www.googleapis.com/auth/userinfo.profile", "https://www.googleapis.com/auth/userinfo.email", "openid"],
    redirect_uri = "http://localhost:5000/callback"
    )

def login_is_required(function):
    def wrapper(*args, **kwargs):
        if "google_id" not in session:
            return abort(401) # authorization required
        else:
            return function()
    
    return wrapper



@app.route("/login")
def login():
    authorization_url, state = flow.authorization_url()
    session["state"] = state
    return redirect(authorization_url)


@app.route("/callback")
def callback():
    flow.fetch_token(authorization_response=request.url)


    if not session["state"] == request.args["state"]:
        abort(500)

    credentials = flow.credentials
    request_session = requests.session()
    cached_session = cachecontrol.CacheControl(request_session)
    token_request = google.auth.transport.requests.Request(session=cached_session)

    id_info = id_token.verify_oauth2_token(
        id_token = credentials._id_token,
        request = token_request,
        audience = GOOGLE_CLIENT_ID
    )

    info = requests.get('http://coupon-manager-api:8081/coupon')
    info = unicodedata.normalize('NFKD', info.text).encode('ascii','ignore')
    info = json.loads(info)

    return render_template('dashboard.html', info=info)

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

@app.route("/")
def index():
    return "logga in <a href='/login'>logga in</a>"

@app.route("/dashboard")
@login_is_required
def dashboard():
    return "Dashboard <a href='/logout'>logga ut</a>"


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0",port=5000)