from Util.SpotifyRequest.browse_request import *

def get_recommended_songs_forall(auth_code, songs):
    rec_songs = list()
    for song in songs:
        rec_songs.extend(get_recommended_songs_for(auth_code, song))
    return rec_songs

def get_recommended_songs_for(auth_code, song):
    return get_recommendations_seed(auth_code, [], [], [song.id])
