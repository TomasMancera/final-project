import numpy as np
from randomNumbers.i_number_solver import INumberRandomSolver

class UniformRandomDistribution(INumberRandomSolver):

    def get_numbers(self, min, max, cant):
        
        numbers = np.random.uniform(min, max, cant)
        int_numbers = numbers.astype(int)
        return int_numbers.tolist()