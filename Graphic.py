import tkinter as tk
from numpy import *
from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class Graphic:
    def __init__(self, equation):
        self.equation = equation.replace("^", "**")
        f = vectorize(self.function)
        x = linspace(-10, 10, 100)
        figure = plt.figure(figsize=(4, 4), dpi=100)
        figure.add_subplot(111).plot(x, f(x), color="red")
        self.chart = FigureCanvasTkAgg(figure)
        self.chart.get_tk_widget().grid(row=4, column=3, columnspan=2, rowspan=8, sticky='n')
        plt.grid(True)
        plt.xlim([-10, 10])
        plt.ylim([-10, 10])
        plt.axhline(linewidth=2, color='black')
        plt.axvline(linewidth=2, color='black')

    def function(self, x):
        seterr(all='warn')
        return eval(self.equation).real
