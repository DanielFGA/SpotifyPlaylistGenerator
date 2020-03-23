import numpy as np

from Util.MachineLearning.matrix import Matrix

CLASS_1 = -1
CLASS_2 = 1

class GaussianDiscriminantAnalysis(object):
    
    def __init__(self, matrix_gda):
        self.matrix_gda = Matrix(matrix_gda)
        self.check_for_zero()
        my_1 = self.my(-1)
        my_2 = self.my(1)
        self.my = {
            -1: my_1,
            1: my_2
        }
        self.sigma = self.sigma()

    def check_for_zero(self):
        for y in range(len(self.matrix_gda.matrix_gda)):
            for x in range(len(self.matrix_gda.matrix_gda[y])):
                if self.matrix_gda.matrix_gda[y,x] == 0:
                    self.matrix_gda.matrix_gda[y,x] += 0.00000000000001
     
    #prob. that a class is found
    def phi(self, c):
        return (1 / self.matrix_gda.y_len()) * self.matrix_gda.count_class(c)
    
    #mean vector for attributes of a class
    def my(self, c): #c = Searched class
        num, det = self.matrix_gda.get_x_attr(0) * 0, self.matrix_gda.get_all_for_class(c).y_len()
        for i in range(self.matrix_gda.get_all_attributes_for_class(c).y_len()):
            num += self.matrix_gda.get_all_attributes_for_class(c).get(i) 
        return num / det
    
    #covariance
    def sigma(self):
        ret = Matrix([[0 for x in range(self.matrix_gda.x_len() - 1)] for y in range(self.matrix_gda.x_len() - 1)])
        new_matrix = []
        for row in self.matrix_gda.matrix_gda:
            new_matrix.append(row[:-1])
        for i in range(self.matrix_gda.y_len()):
            if (self.matrix_gda.get_class(i) == CLASS_1):
                x_vector = (self.matrix_gda.get_x_attr(i) - self.my[CLASS_1])
                ret+= x_vector.transpose().matrix_mult(x_vector)
            else:
                x_vector = (self.matrix_gda.get_x_attr(i) - self.my[CLASS_2])
                ret+= x_vector.transpose().matrix_mult(x_vector)
        return (1 / self.matrix_gda.x_len()) * ret

    #Gaussian Discriminant Analysis
    def gda(self, c, X): #c = Searched class, X = object
        X = X.get_x_attr(0)
        term_1 = 1 / (((2 * np.pi) ** (self.matrix_gda.get_x_attr(0).x_len() / 2)) * (self.sigma.determinate() ** (0.5)))
        term_2 = ((-0.5) * (X - self.my[c])).matrix_mult(self.sigma.inverse()).matrix_mult((X - self.my[c]).transpose())
        result = term_1 * np.exp(term_2.get_matrix()[0][0])
        return result

    def classify(self, X):
        if (self.gda(CLASS_2, X) > self.gda(CLASS_1, X)):
            return CLASS_2
        else:
            return CLASS_1