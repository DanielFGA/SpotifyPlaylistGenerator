from Util.SpotifyRequest.browse_request import *


def collect_recommended_songs(auth_code, songs, rounds):
    # this is the best way to gather many songs without brute force
    collected_songs = list()
    iterations_songs = get_recommended_songs_for_all(auth_code, songs)
    collected_songs.extend(iterations_songs)

    for _ in range(rounds):
        iterations_songs = get_recommended_songs_for_all(auth_code, iterations_songs)
        collected_songs.extend(iterations_songs)

    return list(set(collected_songs))


def get_recommended_songs_for_all(auth_code, songs):
    rec_songs = list()
    for song in songs:
        rec_songs.extend(get_recommended_songs_for(auth_code, song))
    return rec_songs


def get_recommended_songs_for(auth_code, song):
    return get_recommendations_seed(auth_code, [], [], [song.id])
