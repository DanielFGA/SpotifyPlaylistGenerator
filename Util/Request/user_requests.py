import requests
import json
import webbrowser
import random
import string

def read_properties():
    properties = open('settings.properties', 'r').read()
    dict = {}
    for line in properties.split('\n'):
        prop = line.split('=')
        dict[prop[0]] = prop[1]
    return dict

def get_user_permission():
    config = read_properties()
    url = "https://accounts.spotify.com/authorize?client_id={}&response_type={}&redirect_uri={}&scope={}&state={}"
    client_id = config.get("ClientID")
    redirect_url = config.get("AuthCallback")
    secure_string = ''.join(random.choices(string.ascii_uppercase + string.ascii_lowercase + string.digits, k=10))
    scopes = "user-read-private%20user-read-email%20user-library-read%20playlist-modify-public%20playlist-modify-private"
    url = url.format(client_id, "code", redirect_url, scopes, secure_string)
    webbrowser.open(url)
    return secure_string

def get_access_token(code):
    config = read_properties()
    client_id = config.get("ClientID")
    client_secret = config.get("ClientSecret")
    data = {
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': config.get("AuthCallback")
    }
    url = "https://accounts.spotify.com/api/token"
    post_song_response = requests.post(url, data=data, auth=(client_id, client_secret))
    return json.loads(post_song_response.text).get("access_token")

def get_user_info(auth_token):
    get_me_url = "https://api.spotify.com/v1/me"
    header = "Bearer {}"
    get_me_response = json.loads(requests.get(get_me_url, headers={'Authorization': header.format(auth_token)}).text)
    return get_me_response.get("id"), get_me_response.get("display_name")