# flask config

# google oauth2
CLIENT_SECRETS_FILE = 'client_secret.json'
SCOPES = [
    'https://www.googleapis.com/auth/photoslibrary.readonly',
    'https://www.googleapis.com/auth/userinfo.email',
    'https://www.googleapis.com/auth/userinfo.profile',
    'https://www.googleapis.com/auth/plus.me'
]
# google photos api base url
API_BASE_URL = 'https://photoslibrary.googleapis.com/v1'

# downloaded images directory
DOWNLOADED_PHOTOS_LOCATION = 'downloaded/'
