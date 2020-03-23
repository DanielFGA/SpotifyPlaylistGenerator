class Playlist(object):

    def __init__(self, id, name):
        self.name = name
        self.id = id

    def set_songs(self, songs):
        self.songs = songs

    def get_playlist_songs_ids(self):
        ids = list()
        for song in self.songs:
            ids.append(song.id)
        return ids

    def __repr__(self):
        return "[Playlist: {}]".format(self.name)