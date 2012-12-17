from dropbox import client, rest, session


"""
A wrapper class to the Dropbox API.

TODO:
- Integrate mechanize?
- Add isAuthenticated function
"""


class Dropbox(object):

    def __init__(self, app_key=None, app_secret=None, access_type=None):
        self.app_key = app_key
        self.app_secret = app_secret
        self.access_type = access_type
        self.session = None
        self.client = None

    def set_app_key(self, key):
        self.app_key = key

    def set_app_secret(self, secret):
        self.app_secret = secret

    def set_access_type(self, access_type):
        self.access_type = access_type

    def start_session(self):
        self.session = session.DropboxSession(self.app_key, self.app_secret, \
            self.access_type)

    def get_session(self):
        return self.session

    def start_client(self, session):
        self.client = client.DropboxClient(session)

    def get_client(self):
        return self.client

    # Authenticate Dropbox app and store the user's access token key and secret
    # to a file.
    def authenticate(self):
        session = self.get_session()

        # Get a request token
        request_token = session.obtain_request_token()

        auth_url = session.build_authorize_url(request_token)

        # Sign in and authorize this token
        print "url:", auth_url
        print "Please visit this website and press the 'Allow' button, then hit 'Enter' here."
        raw_input()

        access_token = session.obtain_access_token(request_token)
        self.save_access_token(access_token)

    # Save the user access token.
    def save_access_token(self, token):
        # TODO: Encrypt access token key and secret
        with open('dropbox_token.txt', 'wb') as f:
            f.write("%s|%s" % (token.key, token.secret))

    # Load an user's access token from existing file and set the Dropbox
    # client session.
    def connect(self):
        session = self.get_session()

        access_key, access_secret = self.load_user_token()

        session.set_token(access_key, access_secret)
        # TODO: Check for errors raised
        self.start_client(session)

    # Load and return the key and secret of the saved access token.
    def load_user_token(self):
        with open('dropbox_token.txt', 'rb') as f:
            key, secret = f.read().split('|')

        return key, secret

    def upload_file(self, path, filename):
        f = open(filename)
        dropbox_client = self.get_client()
        response = dropbox_client.put_file(path + filename, f)
        return response


if __name__ == "__main__":
    pass
