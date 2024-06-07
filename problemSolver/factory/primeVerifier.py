from .i_problem_solver import IProblemSolver

class PrimeVerifier(IProblemSolver):

    def solve_problem(self, data):
        list_result = []
        for num in data:
            result = self.prime_classifier(int(num))
            list_result.append(str(num) + " " + str(result))

        return list_result

    def prime_classifier(self,number):
        if self.is_prime(number):
            return "prime"
        if self.is_cuadratic_semiprime(number):
            return "cuadratic semiprime"
        if self.is_semiprime(number):
            return "semiprime"
        return number

    def is_prime(self, number):
        count = 0
        for i in range(2,number + 1):

            if (number % i) == 0:
                count +=1

        if count <2:
            return True

        return False

    def is_semiprime(self, number):
        count = 0
        divisor = []
        for i in range(2,number):
            if (number % i) == 0 and self.is_prime(i):
                divisor.append(i)
                count +=1

        if count == 2 and divisor[0]* divisor[1] == number:

            return True

        return False

    def is_cuadratic_semiprime(self, number):
        for i in range(2,number + 1):
            if (number % i) == 0 and self.is_prime(i):
                if (i*i) == number:
                    return True
        return False