from numpy import *
from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


# Клас, який представляє графік трансцендентної функції
class Graphic:
    # Конструктор
    def __init__(self, equation):
        self.equation = equation.replace("^", "**")
        if self.equation == "":
            self.figure = plt.figure(figsize=(4, 4), dpi=100)
        else:
            f = vectorize(self.function)
            x = linspace(-10, 10, 100)
            self.figure = plt.figure(figsize=(4, 4), dpi=100)
            self.figure.add_subplot(111).plot(x, f(x), color="red")
        self.chart = FigureCanvasTkAgg(self.figure)
        plt.grid(True)
        plt.xlim([-10, 10])
        plt.ylim([-10, 10])
        plt.axhline(linewidth=2, color='black')
        plt.axvline(linewidth=2, color='black')

    # Метод для отримання значення трансцендентної фунції у вказаній точці "х"
    def function(self, x):
        seterr(all='warn')
        return eval(self.equation).real
