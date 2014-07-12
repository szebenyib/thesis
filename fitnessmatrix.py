__author__ = 'szebenyib'

import numpy as np


class FitnessMatrix():
    """Numpy array of fitness values. Rows are generations.
    Columns are individuals."""

    def __init__(self, evo, matrix=None):
        """The matrix size is determined by the evo evolution
        parameter dictionary, which should contain 'NGEN' and
        'N' as keys with values."""
        self.evo = evo
        if matrix is None:
            self.matrix = np.zeros((evo.get('NGEN') + 1, evo.get('N')))
        else:
            #Used only by get_copy() method
            self.matrix = matrix

    def save_fitnesses(self, population):
        """Saves the fitness values of the population to the
        next non 0 beginning row of the array."""
        row = 0
        while self.matrix[row][0] > 0:
            row += 1
        for i in range(self.evo.get('N')):
            self.matrix[row][i] = population[i].fitness.values[0]

    def truncate_fitnesses(self, by_max=None, by_min=None):
        """Truncates the fitness values in the fitness matrix.
        If the FitnessMatrix[][] value is *larger* than by_max
        or (inclusive) *smaller* than by_min then it will be
        truncated to the respective by_max and by_min value."""
        if by_max is not None:
            for i in range(self.matrix.shape[0]):
                for j in range(self.matrix.shape[1]):
                    if self.matrix[i][j] > by_max:
                        self.matrix[i][j] = by_max
        if by_min is not None:
            for i in range(self.matrix.shape[0]):
                for j in range(self.matrix.shape[1]):
                    if self.matrix[i][j] < by_min:
                        self.matrix[i][j] = by_min

    def order_fitnesses(self):
        """Orders the fitness values of each generation from
        low to high."""
        return self.matrix.sort(axis=1)

    def get_copy(self):
        """Returns a copy of the instance."""
        return FitnessMatrix(self.evo, self.matrix.copy())

    def get_generation(self, i):
        """Returns a subarray.
        If i is invalid, None is returned."""
        if 0 <= i < self.evo.get('NGEN'):
            return self.matrix[i]
        else:
            return None

    def get_inner_matrix(self):
        """Gets the inner matrix. Mainly to offer the necessary
        numpy array for printing."""
        return self.matrix