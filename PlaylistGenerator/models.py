# Create your models here.
class User(object):

    def __init__(self):
        self.auth_code = ""
        self.access_token = ""
        self.secure_string = ""
        self.id = ""
        self.display_name = ""
        self.songs = list()
        self.playlists = list()

    def set_auth_code(self, auth_code):
        self.auth_code = auth_code

    def set_access_token(self, access_token):
        self.access_token = access_token

    def set_secure_string(self, secure_string):
        self.secure_string = secure_string

    def set_id(self, id):
        self.id = id;

    def set_display_name(self, display_name):
        self.display_name = display_name

    def set_songs(self, songs):
        self.songs = songs

    def set_playlists(self, playlists):
        self.playlists = playlists

    def __repr__(self):
        return "auth_code={}, access_token={}, secure_string={}".format(self.auth_code, self.access_token, self.secure_string)
