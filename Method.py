from numpy import *
from tkinter.messagebox import showwarning


# Абстракний клас, який предсталяє метод розв'язку трансцендентного рівняння
class Method:
    # Конструктор
    def __init__(self, equation):
        self.equation = equation.replace("^", "**")

    # Метод для отримання значення трансцендентної фунції у вказаній точці "х"
    def function(self, x):
        seterr(all='raise')
        return eval(self.equation).real
