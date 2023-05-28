from tkinter.messagebox import showinfo
from BisectMethod import *
from NewtonMethod import *
from SecantMethod import *


class Statistics(BisectMethod, NewtonMethod, SecantMethod):
    def __init__(self, equation, a, b, tolerance, initial_guess, max_iterations):
        BisectMethod.__init__(self, equation, a, b, tolerance)
        NewtonMethod.__init__(self, equation, initial_guess, tolerance, max_iterations)
        SecantMethod.__init__(self, equation, a, b, tolerance, max_iterations)

    def get_statistics(self):
        self.b_solve()
        self.n_solve()
        self.s_solve()
        message = "Метод половинного ділення: "
        message += str(self.b_iterations)
        message += "\nМетод Ньютона: "
        message += str(self.n_iterations)
        message += "\nМетод січних: "
        message += str(self.s_iterations)
        showinfo("Аналітика", message)

