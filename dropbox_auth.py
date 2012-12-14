from dropbox import client, rest, session

DROPBOX_APP_KEY = 'INSERT_APP_KEY_HERE'
DROPBOX_APP_SECRET = 'INSERT_SECRET_HERE'
DROPBOX_ACCESS_TYPE = 'dropbox'

dropbox_session = session.DropboxSession(DROPBOX_APP_KEY, DROPBOX_APP_SECRET, DROPBOX_ACCESS_TYPE)

# Get a request token
dropbox_request_token = dropbox_session.obtain_request_token()

dropbox_auth_url = dropbox_session.build_authorize_url(dropbox_request_token)
# Sign in and authorize this token
print "url:", dropbox_auth_url
print "Please visit this website and press the 'Allow' button, then hit 'Enter' here."
raw_input()

dropbox_access_token = dropbox_session.obtain_access_token(dropbox_request_token)

# TODO: Store Access Token
dropbox_client = client.DropboxClient(dropbox_session)
