from .i_problem_solver import IProblemSolver

class Fibonnaci(IProblemSolver):
    def compute_results(self,data:any) -> any:
        result = []
        for element in data:
            fibonacciResult = self.__fibonacci((element))
            result.append(f"{element} {fibonacciResult}")
        return result

    def __fibonacci(self,num:int) -> any:    
        if num < 0:  
            return False  
        a, b = 0, 1
        if num == a or num == b:
            return True
    
       
        while b < num:
            a, b = b, a + b
            if b == num:
                return True
    
        return False
