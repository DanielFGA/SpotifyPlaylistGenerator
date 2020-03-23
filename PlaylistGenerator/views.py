from django.http import HttpResponse

from PlaylistGenerator.models import User
from Util.Spotify.Browse.recommended_songs import get_recommended_songs_forall
import Util.Request.requests as rq
from Util.Spotify.Playlist.random_playlist import classify_songs

user = User()

def start(request):
    user.set_secure_string(rq.get_user_permission())
    return HttpResponse(status=204)

def authorizes_access(request):
    code = request.GET.get("code")
    state = request.GET.get("state")

    if (state == user.secure_string):
        user.set_auth_code(code)
        user.set_access_token(rq.get_access_token(code))
        user_id, user_display_name = rq.get_user_info(user.access_token)
        user.set_id(user_id)
        user.set_display_name(user_display_name)

    playlists = rq.get_playlists(user.access_token)

    all_songs = list()
    all_songs.extend(rq.get_playlists_songs(user.access_token, playlists))
    all_songs.extend(rq.get_favorites_songs(user.access_token))
    all_songs.extend(get_recommended_songs_forall(user.access_token, all_songs))

    all_songs = set(all_songs)
    all_songs = sorted(all_songs)

    rq.set_features_for_songs(user.access_token, all_songs)

    good_songs = None
    bad_songs = None

    for playlist in playlists:
        if playlist.name == "Fucking Post-Hardcore":
            good_songs = playlist.get_playlist_songs_ids()
        if playlist.name == "EDM/Party":
            bad_songs = playlist.get_playlist_songs_ids()

    fitting_songs = classify_songs(all_songs, good_songs, bad_songs)

    new_playlist_id = rq.create_playlist("test", "test", True, user.access_token, user.id)

    rq.add_songs_to_playlist(user.access_token, fitting_songs, new_playlist_id)


    return HttpResponse(status=204)