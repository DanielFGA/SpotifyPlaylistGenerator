import json

import requests

from Util.Model.song import Song
from Util.SpotifyRequest.requests import concat_parameter, generate_parameter


def get_recommendations_seed(auth_token, seed_artist, seed_genres, seed_tracks):
    if (len(seed_artist) == 0 and len(seed_genres) == 0 and len(seed_tracks) == 0):
        return list()

    songs = list()
    url = "https://api.spotify.com/v1/recommendations?{}"
    url_parameter = concat_parameter([
        generate_parameter("seed_artists", seed_artist, "%2C"),
        generate_parameter("seed_genres", seed_genres, "%2C"),
        generate_parameter("seed_tracks", seed_tracks, "%2C")], "&")
    header = "Bearer {}"

    get_recommendations_seed_response = requests.get(url.format(url_parameter),
                                                     headers={'Authorization': header.format(auth_token)})

    while (get_recommendations_seed_response.status_code != 200):
        get_recommendations_seed_response = requests.get(url.format(url_parameter),
                                                         headers={'Authorization': header.format(auth_token)})

    for response_song in json.loads(get_recommendations_seed_response.text).get("tracks"):
        new_song = Song(
            response_song.get("id"),
            response_song.get("name"),
            response_song.get("artists")[0].get("name")
        )
        songs.append(new_song)

    return songs
