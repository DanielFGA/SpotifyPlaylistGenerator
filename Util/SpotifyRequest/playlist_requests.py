import json

import requests

from Util.Model.playlist import Playlist
from Util.Model.song import Song
from Util.SpotifyRequest.requests import header


def get_playlists(auth_token):
    url = "https://api.spotify.com/v1/me/playlists"
    playlists = list()
    response = requests.get(url, headers={'Authorization': header.format(auth_token)})

    for response_item in json.loads(response.text).get("items"):
        playlists.append(Playlist(response_item.get("id"), response_item.get("name"),
                                  response_item.get("external_urls").get("spotify")))

    return playlists


def get_playlists_songs(auth_token, playlists):
    songs = list()

    for playlist in playlists:
        playlist_songs = get_playlist_songs(auth_token, playlist)
        playlist.set_songs(playlist_songs)
        songs.extend(playlist_songs)
    return songs


def get_playlist_songs(auth_token, playlist):
    url = "https://api.spotify.com/v1/playlists/{}/tracks?limit={}&offset={}"
    songs = list()
    offset = 0
    limit = 50
    get_playlist_songs_response = requests.get(url.format(playlist.id, limit, offset),
                                               headers={'Authorization': header.format(auth_token)})

    while (len(json.loads(get_playlist_songs_response.text).get("items"))):

        for response_item in json.loads(get_playlist_songs_response.text).get("items"):
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
        get_playlist_songs_response = requests.get(url.format(playlist.id, limit, offset),
                                                   headers={'Authorization': header.format(auth_token)})

    return songs


def create_playlist(name, describtion, public, auth_token, user_id):
    data = json.dumps({
        'name': name,
        'description': describtion,
        'public': public
    })
    url = "https://api.spotify.com/v1/users/{user_id}/playlists".format(user_id=user_id)

    response = requests.post(url=url, data=data, headers={'Authorization': header.format(auth_token)})
    response_json = json.loads(response.text)
    return Playlist(response_json.get("id"), name, response_json.get("external_urls").get("spotify"))


def add_songs_to_playlist(auth_token, songs, playlist_id):
    if (len(songs) > 50):
        i = 0
        while (i < len(songs)):
            add_songs_to_playlist(auth_token, songs[i:i + 50], playlist_id)
            if i + 50 >= len(songs):
                i += len(songs) - i
            else:
                i += 50
    else:
        songs_uri = ""
        for song in songs:
            songs_uri += "spotify%3Atrack%3A{}%2C".format(song.id)
        songs_uri = songs_uri[:-3]

        url = "https://api.spotify.com/v1/playlists/{playlist_id}/tracks?uris={tracks}".format(playlist_id=playlist_id,
                                                                                               tracks=songs_uri)

        requests.post(url=url, headers={'Authorization': header.format(auth_token)})
