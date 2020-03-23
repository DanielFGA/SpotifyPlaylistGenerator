import numpy as np

class Song(object):

    def __init__(self, id, name, artist):
        self.id = id
        self.name = name
        self.artist = artist
        self.my_class = 0;

    def set_features(self, features):
        self.features = features

    def get_feature_vector_with_class(self):
        features = self.features.get_as_vector()
        return np.append(features, self.my_class)

    def get_feature_vector(self):
        return self.features.get_as_vector()

    def set_feature(self, feature, value):
        self.features.set_feature(feature, value)

    def __repr__(self):
        return "[Song {} from {}]".format(self.name, self.artist)

    def __lt__(self, other):
        if (self.name == other.name):
            if (self.artist == other.artist):
                return self.id < other.id
            else:
                return self.artist < other.artist
        else:
            return self.name < other.name

    def __eq__(self, other):
        return ((self.name == other.name and self.artist == other.artist) or self.id == other.id)

    def __hash__(self):
        return hash((self.name, self.artist))


class Features(object):

    def __init__(self, danceability, energy, acousticness, liveness, valence, tempo):
        round_digits = 5
        self.danceability = check_for_zero_value(round(danceability, round_digits))
        self.energy = check_for_zero_value(round(energy, round_digits))
        self.acousticness = check_for_zero_value(round(acousticness, round_digits))
        self.liveness = check_for_zero_value(round(liveness, round_digits))
        self.valence = check_for_zero_value(round(valence, round_digits))
        self.tempo = check_for_zero_value(round(tempo, round_digits))
        self.feature_vector = np.array([self.danceability, self.energy, self.acousticness, self.liveness, self.valence, self.tempo])

    def get_as_vector(self):
        return self.feature_vector

    def set_feature(self, feature, value):
        self.feature_vector[feature] = value

def check_for_zero_value(value):
        if (value == 0):
            return value + 0.0001
        else:
            return value