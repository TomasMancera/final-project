# Module docstring

from abc import ABC, abstractmethod

class IProblemSolver(ABC):
    """Abstract base class defining methods for solving problems."""

    @abstractmethod
    def compute_results(self, data):
        pass
        """
        Computes and returns results for a given list of data.
        Args:
            data (list): The data on which computations are to be performed.
        Returns:
            list: The results of the computations.
        """   
    
        