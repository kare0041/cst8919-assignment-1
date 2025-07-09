# 📁 server.py -----

import json
import logging # Import the logging module
from os import environ as env
from urllib.parse import quote_plus, urlencode
from functools import wraps
from datetime import datetime # Added for timestamp

from authlib.integrations.flask_client import OAuth
from dotenv import find_dotenv, load_dotenv
from flask import Flask, redirect, render_template, session, url_for

from flask import request
from werkzeug.middleware.proxy_fix import ProxyFix


# 👆 We're continuing from the steps above. Append this to your server.py file.

ENV_FILE = find_dotenv()
if ENV_FILE:
    load_dotenv(ENV_FILE)

# 👆 We're continuing from the steps above. Append this to your server.py file.

app = Flask(__name__)
app.secret_key = env.get("APP_SECRET_KEY")

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# 👆 We're continuing from the steps above. Append this to your server.py file.

# Make Flask aware it's behind a proxy (like Azure)
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1)

# Optional: redirect HTTP to HTTPS if needed
@app.before_request
def enforce_https_in_production():
    if not request.is_secure and not app.debug:
        url = request.url.replace("http://", "https://", 1)
        return redirect(url, code=301)

oauth = OAuth(app)

oauth.register(
    "auth0",
    client_id=env.get("AUTH0_CLIENT_ID"),
    client_secret=env.get("AUTH0_CLIENT_SECRET"),
    client_kwargs={
        "scope": "openid profile email",
    },
    server_metadata_url=f'https://{env.get("AUTH0_DOMAIN")}/.well-known/openid-configuration'
)

# 👆 We're continuing from the steps above. Append this to your server.py file.

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user' not in session:
            app.logger.warning(f"Unauthorized access attempt at {datetime.now()}") # Log unauthorized attempt
            return redirect('/login')
        return f(*args, **kwargs)
    return decorated_function

@app.route("/login")
def login():
    return oauth.auth0.authorize_redirect(
        redirect_uri=url_for("callback", _external=True)
    )

# 👆 We're continuing from the steps above. Append this to your server.py file.

@app.route("/callback", methods=["GET", "POST"])
def callback():
    token = oauth.auth0.authorize_access_token()
    session["user"] = token
    user_info = session.get('user')
    if user_info:
        user_id = user_info.get('userinfo', {}).get('sub')
        email = user_info.get('userinfo', {}).get('email')
        app.logger.info(f"User login: user_id={user_id}, email={email}, timestamp={datetime.now()}") # Log successful login
    return redirect("/")

# 👆 We're continuing from the steps above. Append this to your server.py file.

@app.route("/logout")
def logout():
    session.clear()
    return redirect(
        "https://" + env.get("AUTH0_DOMAIN")
        + "/v2/logout?"
        + urlencode(
            {
                "returnTo": url_for("home", _external=True),
                "client_id": env.get("AUTH0_CLIENT_ID"),
            },
            quote_via=quote_plus,
        )
    )

# 👆 We're continuing from the steps above. Append this to your server.py file.

@app.route("/")
def home():
    return render_template("home.html", session=session.get('user'), pretty=json.dumps(session.get('user'), indent=4))

@app.route("/protected")
@login_required
def protected():
    user_info = session.get('user')
    if user_info:
        user_id = user_info.get('userinfo', {}).get('sub')
        email = user_info.get('userinfo', {}).get('email')
        app.logger.info(f"Protected route accessed by user: user_id={user_id}, email={email}, timestamp={datetime.now()}") # Log protected route access
    return render_template("protected.html", session=session.get('user'))

# 👆 We're continuing from the steps above. Append this to your server.py file.

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=env.get("PORT", 3000))

