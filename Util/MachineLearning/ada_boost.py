import numpy as np

class AdaBoost(object):

    def __init__(self, dataset, weak_classifiers):
        self.distrubution = [1 / len(dataset)] * len(dataset)
        self.dataset = dataset
        self.choosen_classifier = []
        self.weak_classifier = weak_classifiers

    def train(self):
        self.error = np.zeros(shape=len(self.weak_classifier))

        for h in range(0, len(self.weak_classifier)):
            for i in range(0, len(self.dataset)-1):
                self.error[h] += self.distrubution[i] *(self.delta(self.weak_classifier[h], self.dataset[i][:-1], self.dataset[i][9]))

        self.min_error = self.error.argmin()
        self.alpha_current = self.calc_alpha(self.min_error)
        self.choosen_classifier.append([self.error.argmin(), self.calc_alpha(self.min_error)])
        self.update_dist()

    def delta(self, classifier, X, y):
        y_predict = classifier.classify(X)
        if (y_predict == y):
            return 0
        else:
            return 1

    def calc_alpha(self, t):
        self.alpha = 0.5 * np.log((1 - self.error[self.min_error]) / self.error[self.min_error])
        return self.alpha

    def update_dist(self):
        for i in range(0, len(self.dataset)):
            X = self.dataset[i][:-1]
            y_i_predict = self.weak_classifier[self.min_error].classify(X)
            y_i = self.dataset[i][9]
            alpha = self.alpha_current
            self.distrubution[i] = (self.distrubution[i] * np.exp(-alpha * y_i * y_i_predict)) /  (1 / np.sum(self.distrubution))

    def final(self, X):
        for classifer in self.choosen_classifier:
            sum+= classifer[1] * self.weak_classifier[classifer[0]].classify(X)
        return np.sign(sum)

class WeakSongClassifier(object):

    def __init__(self, feature_selection, threshold):
        self.feature_selection = feature_selection;
        self.thresholds = threshold

    def classify(self, X):
        if (X[self.feature_selection] >= self.threshold):
            return -1
        else:
            return 1

    def __repr__(self):
        return "feature_selection = {}, threshold = {}".format(self.feature_selection, self.threshold)