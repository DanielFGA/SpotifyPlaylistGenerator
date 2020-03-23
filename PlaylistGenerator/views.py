from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader

import Util.Request.requests as rq
from PlaylistGenerator.models import User
from Util.Spotify.Browse.recommended_songs import get_recommended_songs_forall
from Util.Spotify.Playlist.random_playlist import classify_songs

user = User()

def start(request):
    template = loader.render_to_string('PlaylistGenerator/start.html')
    return HttpResponse(template)

def auth_start(request):
    secure_string, url =  rq.get_user_permission()
    user.set_secure_string(secure_string)
    return HttpResponseRedirect(url)

def get_spotify_access(request):
    user.set_secure_string(rq.get_user_permission())
    return HttpResponse(status=204)

def authorizes_access(request):
    template = loader.get_template('PlaylistGenerator/select.html')
    code = request.GET.get("code")
    state = request.GET.get("state")

    if (state == user.secure_string):
        user.set_auth_code(code)
        user.set_access_token(rq.get_access_token(code))
        user_id, user_display_name = rq.get_user_info(user.access_token)
        user.set_id(user_id)
        user.set_display_name(user_display_name)

    playlists = rq.get_playlists(user.access_token)
    playlists = sorted(playlists)

    songs = rq.get_favorites_songs(user.access_token)
    songs.extend(rq.get_playlists_songs(user.access_token, playlists))
    songs = set(songs)
    songs = sorted(songs)

    user.set_songs(songs)
    user.set_playlists(playlists)

    context = {
        'playlists' : playlists,
        'songs': songs
    }

    return HttpResponse(template.render(context, request))


def generate_playlist(request):
    template = loader.get_template('PlaylistGenerator/finish.html')
    playlist_name = request.GET.get("playlist_name") if len(request.GET.get("playlist_name")) > 0 else "unnamed"
    good_song_ids = request.GET.getlist("song_yes") if request.GET.get("song_yes") else list()
    bad_song_ids = request.GET.getlist("song_no") if request.GET.get("song_no") else list()
    good_playlist_ids = request.GET.getlist("playlist_yes") if request.GET.getlist("playlist_yes") else list()
    bad_playlist_ids = request.GET.getlist("playlist_no") if request.GET.getlist("playlist_no") else list()
    good_songs = list()
    bad_songs = list()

    for user_playlist in user.playlists:
        if user_playlist.id in good_playlist_ids:
            good_songs.extend(rq.get_playlist_songs(user.access_token, user_playlist))
        if user_playlist.id in bad_playlist_ids:
            bad_songs.extend(rq.get_playlist_songs(user.access_token, user_playlist))

    for song in user.songs:
        if song.id in good_song_ids:
            good_songs.append(song)
        if song.id in bad_song_ids:
            bad_songs.append(song)

    user.songs.extend(get_recommended_songs_forall(user.access_token, good_songs))
    rq.set_features_for_songs(user.access_token, user.songs)

    user.set_songs(distict_sorted_list(user.songs))

    fitting_songs = classify_songs(user.songs, good_songs, bad_songs)

    new_playlist = rq.create_playlist(playlist_name, "Generated from ...", False, user.access_token, user.id)

    rq.add_songs_to_playlist(user.access_token, fitting_songs, new_playlist.id)

    context = {
        'playlist_name': new_playlist.name,
        'playlist_link': new_playlist.url,
        'songs': fitting_songs
    }

    return HttpResponse(template.render(context, request))


def distict_sorted_list(unsorted):
    return list(set(sorted(unsorted)))
