import json
import random
import string

import requests

from SpotifyPlaylistGenerator.properties import Properties
from Util.SpotifyRequest.requests import header

config = Properties()


def get_user_permission(scopes):
    url = "https://accounts.spotify.com/authorize?client_id={}&response_type={}&redirect_uri={}&scope={}&state={}"
    client_id = config.client_id
    redirect_url = config.redirect_url
    secure_string = ''.join(random.choices(string.ascii_uppercase + string.ascii_lowercase + string.digits, k=10))
    url = url.format(client_id, "code", redirect_url, '%20'.join(scopes), secure_string)
    # webbrowser.open(url)
    return secure_string, url


def get_access_token(code):
    client_id = config.client_id
    client_secret = config.client_secret
    data = {
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': config.redirect_url
    }
    url = "https://accounts.spotify.com/api/token"
    post_song_response = requests.post(url, data=data, auth=(client_id, client_secret))
    return json.loads(post_song_response.text).get("access_token")


def get_user_info(auth_token):
    get_me_url = "https://api.spotify.com/v1/me"
    get_me_response = json.loads(requests.get(get_me_url, headers={'Authorization': header.format(auth_token)}).text)
    return get_me_response.get("id"), get_me_response.get("display_name")
