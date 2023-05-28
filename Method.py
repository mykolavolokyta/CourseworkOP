from numpy import *
from tkinter.messagebox import showwarning


class Method:
    def __init__(self, equation):
        self.equation = equation.replace("^", "**")

    def function(self, x):
        seterr(all='raise')
        return eval(self.equation).real
