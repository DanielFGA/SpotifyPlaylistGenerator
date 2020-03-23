from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader

from PlaylistGenerator.models import User
from Util.Model.playlist import Playlist
from Util.Spotify.Browse.recommended_songs import get_recommended_songs_forall
import Util.Request.requests as rq
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
    songs = rq.get_favorites_songs(user.access_token)
    songs.extend(rq.get_playlists_songs(user.access_token, playlists))
    songs = set(songs)

    context = {
        'playlists' : playlists,
        'songs': songs
    }
    return HttpResponse(template.render(context, request))
