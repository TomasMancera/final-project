# Module docstring


from typing import List
from .i_problem_solver import IProblemSolver

class FizzBuzz(IProblemSolver):
    """Class for computing FizzBuzz for single values or lists of values."""

    def compute_results(self, data: List[int]) -> List[str]:
        """
        Compute FizzBuzz for a list of integers and return the results.

        Args:
            data (List[int]): A list of integers to compute FizzBuzz for.

        Returns:
            List[str]: A list of strings representing the FizzBuzz results.
        """
        result = []
        for element in data:
            fizzbuzz_result = self.__fizz_buzz(int(element))
            result.append(f"{element} {fizzbuzz_result}")
        return result

    def __fizz_buzz(self, number: int) -> str:
        """
        Helper method to compute the FizzBuzz result for a given number.

        Args:
            number (int): The number to compute FizzBuzz for.

        Returns:
            str: 'Fizz', 'Buzz', 'FizzBuzz', or the number as a string based on FizzBuzz rules.
        """
        result = str(number)
        if number % 3 == 0:
            result = "Fizz"
            if number % 5 == 0:
                result += "Buzz"
        elif number % 5 == 0:
            result = "Buzz"
        return result
