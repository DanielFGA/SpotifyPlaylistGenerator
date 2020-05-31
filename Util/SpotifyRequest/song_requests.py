import json

import requests

from Util.Model.song import Song, Features
from Util.SpotifyRequest.requests import header


def get_favorites_songs(auth_token):
    get_song_url = "https://api.spotify.com/v1/me/tracks?market=DE&limit={}&offset={}"
    songs = list()
    offset = 0
    limit = 50
    get_song_response = requests.get(get_song_url.format(limit, offset),
                                     headers={'Authorization': header.format(auth_token)})

    while (get_song_response.status_code != 502):

        full_response = json.loads(get_song_response.text).get("items")

        if (len(full_response) == 0):
            break

        for response_item in full_response:
            response_song = response_item.get("track")
            if (response_song.get("is_local")):
                continue
            new_song = Song(
                response_song.get("id"),
                response_song.get("name"),
                response_song.get("artists")[0].get("name")
            )
            new_song.is_known = True
            songs.append(new_song)

        offset += limit
        get_song_response = requests.get(get_song_url.format(limit, offset), headers={
            'Authorization': header.format(auth_token)})

    return songs


def get_songs(auth_token, song_ids, is_known):
    get_song_url = "https://api.spotify.com/v1/tracks?ids={}"
    offset = 0
    limit = 50
    step_size = 50
    id_concat_list = list()
    songs = list()

    for id in song_ids:
        id_concat_list.append(id + "%2C")

    while (limit < len(id_concat_list) - 1):
        id_concat = ""

        if limit + step_size > len(id_concat_list):
            limit = len(id_concat_list) - 1
        else:
            limit = limit + step_size

        for id in range(offset, limit):
            id_concat += id_concat_list[id]

        response_songs = json.loads(requests.get(get_song_url.format(id_concat),
                                                 headers={'Authorization': header.format(auth_token)}).text)

        for response_item in json.loads(response_songs.text).get("items"):
            response_song = response_item.get("track")
            if (response_song.get("is_local")):
                continue
            new_song = Song(
                response_song.get("id"),
                response_song.get("name"),
                response_song.get("artists")[0].get("name")
            )
            new_song.is_known = is_known
            songs.append(new_song)
            offset += 1

    return songs

def set_features_for_songs(auth_token, songs):
    get_song_features_url = "https://api.spotify.com/v1/audio-features?ids={}"
    offset = 0
    limit = 0
    step_size = 50
    id_concat_list = list()

    for song in songs:
        id_concat_list.append(song.id + "%2C")

    while limit < len(id_concat_list):
        id_concat = ""

        if limit + step_size > len(id_concat_list):
            limit = len(id_concat_list)
        else:
            limit = limit + step_size

        for id in range(offset, limit):
            id_concat += id_concat_list[id]

        get_feature_response = requests.get(get_song_features_url.format(id_concat),
                                            headers={'Authorization': header.format(auth_token)})

        while (get_feature_response.status_code != 200):
            get_feature_response = requests.get(get_song_features_url.format(id_concat),
                                                headers={'Authorization': header.format(auth_token)})

        response_features = json.loads(get_feature_response.text)

        for feature in response_features.get("audio_features"):
            songs[offset].set_features(Features(
                feature.get("danceability"),
                feature.get("energy"),
                feature.get("acousticness"),
                feature.get("liveness"),
                feature.get("valence"),
                feature.get("tempo"))
            )
            offset += 1