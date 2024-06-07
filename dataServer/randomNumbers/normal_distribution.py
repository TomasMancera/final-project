import numpy as np
from randomNumbers.i_number_solver import INumberRandomSolver

class NormalRandomDistribution(INumberRandomSolver):

    def get_numbers(self, min, max, cant):

        mean = (min + max)/2

        scale = abs(max - min) / 6
        
        numbers = np.random.normal(mean, scale, cant)
        int_numbers = numbers.astype(int)
        return int_numbers.tolist()