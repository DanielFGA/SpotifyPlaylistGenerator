# Create your models here.
from django.db import models


class User(models.Model):
    auth_code = models.CharField(max_length=1000)
    access_token = models.CharField(max_length=1000)
    secure_string = models.CharField(max_length=1000)
    secure_string = models.CharField(max_length=1000)
    user_id = models.CharField(max_length=1000)
    display_name = models.CharField(max_length=1000)

    def set_auth_code(self, auth_code):
        self.auth_code = auth_code

    def set_access_token(self, access_token):
        self.access_token = access_token

    def set_secure_string(self, secure_string):
        self.secure_string = secure_string

    def set_id(self, id):
        self.user_id = id;

    def set_display_name(self, display_name):
        self.display_name = display_name

    def __repr__(self):
        return "auth_code={}, access_token={}, secure_string={}".format(self.auth_code, self.access_token, self.secure_string)
