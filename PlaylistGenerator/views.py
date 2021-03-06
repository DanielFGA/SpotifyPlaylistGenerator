from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader

from PlaylistGenerator.models import User
from Util.Spotify.Browse.recommended_songs import collect_recommended_songs
from Util.Spotify.Playlist.find_fitting_songs import classify_songs
from Util.SpotifyRequest.playlist_requests import *
from Util.SpotifyRequest.song_requests import *
from Util.SpotifyRequest.user_requests import *


def start(request):
    template = loader.render_to_string('PlaylistGenerator/start.html')
    return HttpResponse(template)


def auth_start(request):
    user = User.objects.create()
    secure_string, url = get_user_permission(
        ['user-read-private', 'user-read-email', 'user-library-read', 'playlist-modify-public',
         'playlist-modify-private'])
    user.set_secure_string(secure_string)
    user.save()
    return HttpResponseRedirect(url)


def authorizes_access(request):
    template = loader.get_template('PlaylistGenerator/select.html')
    code = request.GET.get("code")
    secure_string = request.GET.get("state")
    user = User.objects.get(secure_string=secure_string)

    user.set_auth_code(code)
    user.set_access_token(get_access_token(code))
    user_id, user_display_name = get_user_info(user.access_token)
    user.set_id(user_id)
    user.set_display_name(user_display_name)

    user_ups = User.objects.all().filter(user_id=user_id)

    if (len(user_ups) > 0):
        User.objects.all().filter(user_id=user_id).delete()

    user.save()

    playlists, songs = get_playlists_and_songs(user)

    context = {
        'playlists': playlists,
        'songs': songs,
        'secure_string': user.secure_string,
        'display_name': user.display_name
    }

    return HttpResponse(template.render(context, request))


def generate_playlist(request):
    template = loader.get_template('PlaylistGenerator/finish.html')
    algorithm = request.GET.get("algorithm")
    center_numbers = request.GET.get("cluster_number")
    playlist_name = request.GET.get("playlist_name") if len(request.GET.get("playlist_name")) > 0 else "unnamed"
    good_song_ids = request.GET.getlist("song_yes") if request.GET.get("song_yes") else list()
    bad_song_ids = request.GET.getlist("song_no") if request.GET.get("song_no") else list()
    good_playlist_ids = request.GET.getlist("playlist_yes") if request.GET.getlist("playlist_yes") else list()
    bad_playlist_ids = request.GET.getlist("playlist_no") if request.GET.getlist("playlist_no") else list()
    good_songs = list()
    bad_songs = list()
    secure_string = request.GET.get("secure_string")

    user = User.objects.get(secure_string=secure_string)

    playlists, songs = get_playlists_and_songs(user)

    for user_playlist in playlists:
        if user_playlist.id in good_playlist_ids:
            good_songs.extend(get_playlist_songs(user.access_token, user_playlist))
        if user_playlist.id in bad_playlist_ids:
            bad_songs.extend(get_playlist_songs(user.access_token, user_playlist))

    for song in songs:
        if song.id in good_song_ids:
            good_songs.append(song)
        if song.id in bad_song_ids:
            bad_songs.append(song)

    songs.extend(collect_recommended_songs(user.access_token, good_songs, 1))
    set_features_for_songs(user.access_token, songs)

    songs = (distict_sorted_list(songs))

    fitting_songs = classify_songs(songs, good_songs, bad_songs, algorithm)

    fitting_songs = list(filter(lambda x: not x.is_known, fitting_songs))

    new_playlist = create_playlist(playlist_name, "Generated from ... with algorithm {}"
                                   .format(get_algorithm_name(algorithm)), False, user.access_token, user.user_id)

    add_songs_to_playlist(user.access_token, fitting_songs, new_playlist.id)

    context = {
        'playlist_name': new_playlist.name,
        'playlist_link': new_playlist.url,
        'songs': fitting_songs
    }

    return HttpResponse(template.render(context, request))


def get_playlists_and_songs(user):
    playlists = get_playlists(user.access_token)
    playlists = sorted(playlists)

    songs = get_favorites_songs(user.access_token)
    songs.extend(get_playlists_songs(user.access_token, playlists))
    songs = set(songs)
    songs = sorted(songs)

    return playlists, songs


def distict_sorted_list(unsorted):
    return list(set(sorted(unsorted)))


def get_algorithm_name(algorithm):
    if algorithm == "GDA":
        return "Gaussian Discriminant Analysis"
    if algorithm == "Cluster":
        return "Clustering"
    return "... i forgot"
