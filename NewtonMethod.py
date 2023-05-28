from numpy import *
from Method import *
from MethodException import *


class NewtonMethod(Method):
    def __init__(self, equation, initial_guess, tolerance, max_iterations):
        if tolerance <= 0:
            raise MethodException("Точність має бути додатною.")
        if max_iterations <= 0:
            raise MethodException("Кількість ітерацій має бути додатною.")
        Method.__init__(self, equation)
        self.initial_guess = initial_guess
        self.tolerance = tolerance
        self.max_iterations = max_iterations
        self.n_iterations = 0

    def derivative(self, x):
        return (self.function(x + 0.0000001) - self.function(x - 0.0000001)) / (2 * 0.0000001)

    def n_solve(self):
        x = self.initial_guess
        self.n_iterations = 0

        while abs(self.function(x)) > self.tolerance and self.n_iterations < self.max_iterations:
            self.n_iterations += 1
            x = x - self.function(x) / self.derivative(x)

        if abs(self.function(x)) <= self.tolerance:
            return x
        else:
            raise MethodException("Метод не збігся за вказану кількість ітерацій.")
