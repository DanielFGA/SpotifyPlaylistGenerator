import random
import math
import numpy as np

class BinaryClassification(object):

    def __init__(self, training_set, learning_rate):
        self.M = training_set
        self.learning_rate = learning_rate
        self.T = []
        for i in range(4):
            self.T.append(random.uniform(-1.0, 1.0))

    def train(self, runs):
        for run in range(runs):
            self.run()

    def hypothesis(self, x):
        return self.T[0] + (self.T[1] * self.M[x, 0]) + (self.T[2] * self.M[x, 1]) + (self.T[3] * self.M[x, 2])

    def get_class(self,x):
        return self.M[x, 3]

    def sigmoid(self, x):
        return 1 / (1 + np.exp(-x))

    def run(self):
        for i in range(len(self.M)):
            for t in range(len(self.T)):
                self.T[t] = self.T[t] + self.learning_rate * (self.get_class(i) - self.sigmoid(self.hypothesis(i))) * self.check_theta(t, i)

    def check_theta(self, t, x):
        if t == 0:
            return 1
        else:
            return self.M[x][t]

