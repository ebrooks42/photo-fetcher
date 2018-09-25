from gevent import monkey

monkey.patch_all()

import logging
import datetime
from flask import Flask, redirect, session, url_for, request, jsonify, abort
import google_auth_oauthlib.flow
import os

from constants import CLIENT_SECRETS_FILE, SCOPES
from app_secrets import APP_SECRET_KEY
from update_downloaded.update_downloaded_photos import update_downloaded_photos

os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
app = Flask(__name__)
app.secret_key = APP_SECRET_KEY


# application endpoints
@app.route('/')
def index():
    if not valid_credentials():
        return redirect('login')

    try:
        update_downloaded_photos(session['credentials']['token'])
        return jsonify(success=True)
    except Exception:
        logging.exception('Failed to update downloaded photos.')
        abort(500)


@app.route('/clear-session')
def clear_session():
    session.clear()
    return 'Successfully cleared session for current user.'


# authentication endpoints
@app.route('/login')
def login():
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        CLIENT_SECRETS_FILE,
        scopes=SCOPES,
    )
    flow.redirect_uri = url_for('oauth2_callback', _external=True)

    authorization_url, state = flow.authorization_url(
        access_type='offline',
        include_granted_scopes='true',
    )

    session['state'] = state

    return redirect(authorization_url)


@app.route('/oauth2_callback')
def oauth2_callback():
    state = session['state']

    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        CLIENT_SECRETS_FILE,
        scopes=SCOPES,
        state=state,
    )
    flow.redirect_uri = url_for('oauth2_callback', _external=True)

    authorization_response = request.url
    flow.fetch_token(authorization_response=authorization_response)

    credentials = flow.credentials
    session['credentials'] = credentials_to_dict(credentials)

    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run()


def credentials_to_dict(credentials):
    return {
        'token': credentials.token,
        'expiry': credentials.expiry,
        'refresh_token': credentials.refresh_token,
        'token_uri': credentials.token_uri,
        'client_id': credentials.client_id,
        'client_secret': credentials.client_secret,
        'scopes': credentials.scopes
    }


def valid_credentials():
    return 'credentials' in session and \
           'expiry' in session['credentials'] and \
           datetime.datetime.now() < session['credentials']['expiry']
