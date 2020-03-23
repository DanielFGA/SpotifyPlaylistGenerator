class Playlist(object):

    def __init__(self, id, name, url):
        self.name = name
        self.id = id
        self.url = url

    def set_songs(self, songs):
        self.songs = songs

    def get_playlist_songs_ids(self):
        ids = list()
        for song in self.songs:
            ids.append(song.id)
        return ids

    def __repr__(self):
        return "[Playlist: {}]".format(self.name)

    def __lt__(self, other):
        if (self.name == other.name):
            return self.id < other.id
        else:
            return self.name < other.name

    def __eq__(self, other):
        return (self.id == other.id)

    def __hash__(self):
        return hash(self.id)
