from numpy import *
from Method import *
from MethodException import *


class BisectMethod(Method):
    def __init__(self, equation, a, b, tolerance):
        if a >= b:
            raise MethodException("'a' має бути менше за 'b'.")
        if tolerance <= 0:
            raise MethodException("Точність має бути додатною.")
        Method.__init__(self, equation)
        self.a = a
        self.b = b
        self.tolerance = tolerance
        self.b_iterations = 0

    def b_solve(self):
        a = self.a
        b = self.b
        if self.function(a) * self.function(b) >= 0:
            raise MethodException("Значення функції в точках 'a' та 'b' мають мати різні знаки.")
        self.b_iterations = 0
        while abs(b - a) > self.tolerance:
            self.b_iterations += 1
            c = (a + b) / 2
            if self.function(c) == 0:
                return c
            elif self.function(c) * self.function(a) < 0:
                b = c
            else:
                a = c
        return (a + b) / 2
