import numpy as np


class Clustering(object):

    def __init__(self, dataset, centers):
        self.dataset = dataset
        self.centers = centers

    def assign_center(self):
        for data in self.dataset:
            min_dist_center_index = 0
            min_dist = self.euclidean_distance(data[:-1], self.centers[min_dist_center_index])
            for index, center in enumerate(self.centers):
                distance = self.euclidean_distance(data[:-1], center)
                if distance < min_dist:
                    min_dist = distance if distance < min_dist else min_dist
                    min_dist_center_index = index
            data[len(data) - 1] = min_dist_center_index

    def euclidean_distance(self, X_1, X_2):
        terms = []
        for i in range(len(X_2)):
            terms.append((X_2[i] - X_1[i]) ** 2)
        return np.sqrt(sum(terms))
