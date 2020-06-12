from random import randrange

import numpy as np


class KMeans(object):

    def __init__(self, k, dataset):
        self.k = k
        self.dataset_orgin = dataset
        self.amount_data = len(self.dataset_orgin)
        self.center_index = len(self.dataset_orgin[0])
        self.re_init()

    def re_init(self):
        self.dataset = np.copy(self.dataset_orgin)
        # center init: randomly selected points
        self.centre = np.empty([self.k, 3])
        amout_center = 0
        while (amout_center < self.k):
            random_center = randrange(0, self.amount_data)
            if not random_center in self.centre:
                self.dataset[random_center][2] = random_center
                self.centre[amout_center] = self.dataset[random_center]
                amout_center += 1

    def run(self, runs):
        for _ in range(runs):
            self.assign_centre()
            self.re_calc_centre()
        self.assign_centre()

    def euclidean_distance(self, X_1, X_2):
        terms = []
        for i in range(len(X_1)):
            terms.append((X_2[i] - X_1[i]) ** 2)
        return np.sqrt(sum(terms))

    def assign_centre(self):
        for data in range(self.amount_data):
            min_dist_centre = self.get_center_min_dist(data)
            self.dataset[data][self.center_index] = self.centre[min_dist_centre][self.center_index]

    def get_center_min_dist(self, data_index):
        min_dist_centre_index = 0
        min_dist = self.euclidean_distance(self.dataset[data_index], self.centre[0])
        for centre_index in range(self.k):
            dist = self.euclidean_distance(self.dataset[data_index], self.centre[centre_index])
            if dist < min_dist:
                min_dist = dist
                min_dist_centre_index = centre_index
        return min_dist_centre_index

    def re_calc_centre(self):
        centre_mean = np.zeros([self.k, 3])
        for data in range(self.amount_data):
            for i in range(self.k):
                if (self.centre[i][self.center_index] == self.dataset[data][self.center_index]):
                    for y in range(self.center_index - 1):
                        centre_mean[i][y] += self.dataset[data][y]
                    centre_mean[i][self.center_index] += 1

        for i in range(self.k):
            for y in range(self.center_index - 1):
                self.centre[i][y] = centre_mean[i][y] / centre_mean[i][self.center_index]
            self.centre[i][self.center_index] = i + 1

    def __repr__(self):
        return "centers = {c}".format(c=self.centre)
