from numpy import *
from Method import *
from MethodException import *


class SecantMethod(Method):
    def __init__(self, equation, a, b, tolerance, max_iterations):
        if a >= b:
            raise MethodException("'a' має бути менше за 'b'.")
        if tolerance <= 0:
            raise MethodException("Точність має бути додатною.")
        if max_iterations <= 0:
            raise MethodException("Кількість ітерацій має бути додатною.")
        Method.__init__(self, equation)
        self.a = a
        self.b = b
        self.tolerance = tolerance
        self.max_iterations = max_iterations
        self.s_iterations = 0

    def s_solve(self):
        if self.function(self.a) * self.function(self.b) >= 0:
            raise MethodException("Значення функції в точках 'a' та 'b' мають мати різні знаки.")

        x0 = self.a
        x1 = self.b
        self.s_iterations = 0

        while abs(self.function(x1)) > self.tolerance and self.s_iterations < self.max_iterations:
            self.s_iterations += 1
            x2 = x1 - (self.function(x1) * (x1 - x0)) / (self.function(x1) - self.function(x0))
            x0 = x1
            x1 = x2

        if abs(self.function(x1)) <= self.tolerance:
            return x1
        else:
            raise MethodException("Метод не збігся за вказану кількість ітерацій.")
