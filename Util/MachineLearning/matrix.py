import numpy as np


# TODO rewrite
class Matrix(object):

    def __init__(self, matrix):
        self.matrix_gda = []
        if (len(np.array(matrix).shape) == 1):
            self.matrix_gda.append(matrix)
        else:
            self.matrix_gda = matrix
        self.matrix_gda = np.array(self.matrix_gda)

    def get(self, dataset):
        return Matrix(self.matrix_gda[dataset])

    def get_all_for_class(self, c):
        ret = []
        for m in self.matrix_gda:
            if (m[self.x_len() - 1] == c):
                ret.append(m)
        return Matrix(ret)

    def get_all_attributes_for_class(self, c):
        ret = []
        for m in self.matrix_gda:
            if (m[self.x_len() - 1] == c):
                ret.append(m[0:self.x_len() - 1])
        return Matrix(ret)

    def get_x_attr(self, dataset):
        return Matrix(self.matrix_gda[dataset][0:self.x_len() - 1])

    def get_class(self, dataset):
        return self.matrix_gda[dataset][self.x_len() - 1]

    def count_class(self, c):
        counter = 0
        for m in self.matrix_gda:
            if (m[self.x_len() - 1] == c):
                counter += 1
        return counter

    def x_len(self):
        if (len(np.array(self.matrix_gda).shape) == 1):
            return 1
        return len(self.matrix_gda[0])

    def y_len(self):
        return len(self.matrix_gda)

    def matrix_mult(self, matrix_2):
        if (self.x_len() != matrix_2.y_len()):
            return []
        prod_matrix = [[0 for x in range(matrix_2.x_len())] for y in range(self.y_len())]
        for x in range(self.y_len()):
            for y in range(matrix_2.x_len()):
                prod = 0
                for i in range(self.x_len()):
                    prod += self.matrix_gda[x][i] * matrix_2.matrix_gda[i][y]
                prod_matrix[x][y] = prod
        return Matrix(prod_matrix)

    def cut_matrix(self, start, end_right, end_down):
        matrix = []
        for y in range(start[1] - 1, end_down):
            matrix.append(self.matrix_gda[y][start[0] - 1:end_right])
        return matrix(matrix)

    def avg_value(self):
        avg = 0
        counter = 0
        for row in self.matrix_gda:
            for value in row:
                avg += value
                counter += 1
        return avg / counter

    def transpose(self):
        return Matrix(np.transpose(self.matrix_gda))

    def inverse(self):
        return Matrix(np.linalg.inv(self.matrix_gda))

    def determinate(self):
        return np.linalg.det(self.matrix_gda)

    def easy_det(self):
        return (self.matrix_gda[0, 0] * self.matrix_gda[1, 1]) - (self.matrix_gda[1, 0] * self.matrix_gda[0, 1])

    def __add__(self, other):
        return Matrix(self.get_matrix() + other.get_matrix())

    def __sub__(self, other):
        return Matrix(self.get_matrix() - other.get_matrix())

    def __pow__(self, other):
        return Matrix(self.get_matrix() * other)

    def __mul__(self, other):
        return Matrix(self.get_matrix() * other)

    def __rmul__(self, other):
        return Matrix(self.get_matrix() * other)

    def __truediv__(self, other):
        return Matrix(self.get_matrix() / other)

    def __str__(self):
        return str(self.matrix_gda)

    def __repr__(self):
        return str(self.matrix_gda)

    def get_matrix(self):
        return self.matrix_gda

    def set_matrix(self, m):
        self.matrix_gda = np.array(m)

    def is_symmetrical(self):
        if len(self.matrix_gda) != len(self.matrix_gda[0]):
            return False
        for y in range(len(self.matrix_gda)):
            for x in range(len(self.matrix_gda[y])):
                if self.matrix_gda[x, y] != self.matrix_gda[y, x]:
                    return False
        return True
