from itertools import product

import numpy as np

from Util.MachineLearning.ada_boost import WeakSongClassifier, AdaBoost
from Util.MachineLearning.binary_classification_LR import BinaryClassification
from Util.MachineLearning.gaussian_discriminant_analysis import GaussianDiscriminantAnalysis
from Util.MachineLearning.matrix import Matrix


def normalize_function(x, min_x, max_x):
    return (x - min_x) / (max_x - min_x)

def normalize(songs):
    norm_songs = list.copy(songs)
    max_min_init_vector = np.copy(norm_songs[0].get_feature_vector())
    features_length = len(max_min_init_vector)
    max_features =  np.copy(max_min_init_vector)
    min_features =  np.copy(max_min_init_vector)

    for song in norm_songs:
        for i in range(features_length):
            if (max_features[i] < song.get_feature_vector()[i]):
                max_features[i] = song.get_feature_vector()[i]
            if (min_features[i] > song.get_feature_vector()[i]):
                min_features[i] = song.get_feature_vector()[i]

    for song in norm_songs:
        for i in range(features_length):
            song.set_feature(i, normalize_function(song.get_feature_vector()[i], min_features[i], max_features[i]))
    return norm_songs

def cross_features(cross_value, songs):
    all_combinations = []
    crossings = list()
    for offset in range(len(songs[0])-3):
        all_combinations.extend([ele for ele in product(range(offset, cross_value + offset), repeat = cross_value)])

    for triple in all_combinations:
        crossings.append(np.array([songs[:,triple[0]], songs[:,triple[1]], songs[:,triple[2]], songs[:,len(songs)-1]]).transpose())

    return crossings

def generate_weak_classifer(songs):
    classifier = []
    for feature in range(len(songs[0])-1):
        for threshold in np.arange(-1.0, 1.0, 0.1):
            classifier.append(WeakSongClassifier(feature, threshold))
    return classifier

def find_songs_ada_boost(good_songs, bad_songs, songs):

    training_set = []

    for song in songs:
        if (song.name in good_songs):
            song.my_class = 1
        if (song.name in bad_songs):
            song.my_class = -1
        training_set.append(song.get_feature_vector_with_class())

    weaks = generate_weak_classifer(training_set)

    ada_boost = AdaBoost(training_set, weaks)

    for i in range(100):
        ada_boost.train()

    for data in training_set:
        predicted_class = ada_boost.final(data[:-1])
        true_class = data[9]
        print("hi")

def find_songs_binary_classification(good_songs, bad_songs, songs):
    song_matrix_gda = []

    for song in songs:
        if (song.name in good_songs):
            song.my_class = 1
            song_matrix_gda.append(song.get_feature_vector_with_class())
        if (song.name in bad_songs):
            song.my_class = -1
            song_matrix_gda.append(song.get_feature_vector_with_class())

    song_matrix_gda = np.array(song_matrix_gda)

    crossings = cross_features(3, song_matrix_gda)
    class_results = list()

    for cross in crossings:
        classifier = BinaryClassification(cross, 0.001)
        classifier.train(1000)
        #class_results.append(classifier.error())

def find_songs_gda(good_songs, bad_songs, songs):
    song_matrix_gda = []

    for song in songs:
        if (song in good_songs):
            song.my_class = 1
            song_matrix_gda.append(song.get_feature_vector_with_class())
        if (song in bad_songs):
            song.my_class = -1
            song_matrix_gda.append(song.get_feature_vector_with_class())

    song_gda = GaussianDiscriminantAnalysis(song_matrix_gda)
    fitting_songs = list()
    non_fitting_songs = list()

    for song in songs:
        song_feature_vector = Matrix(song.get_feature_vector_with_class())
        fitting_prob = song_gda.gda(1, song_feature_vector)
        non_fitting_prob = song_gda.gda(-1, song_feature_vector)
        if (non_fitting_prob > fitting_prob):
            #print("Dieser Song passt NICHT: {}".format(songs[i]))
            non_fitting_songs.append(song)
        else:
            #print("Dieser Song passt: {}".format(songs[i]))
            fitting_songs.append(song)

    return fitting_songs

def classify_songs(songs, good_songs, bad_songs):
    songs_norm = normalize(songs)
    return find_songs_gda(good_songs, bad_songs, songs_norm)




