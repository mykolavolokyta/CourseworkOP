import tkinter as tk
from numpy import *
from Method import *
from MethodException import *


class NewtonMethod(Method):
    def __init__(self, equation, initial_guess, tolerance, max_iterations):
        if initial_guess < -10000 or initial_guess > 10000:
            raise MethodException("Початкове припущення має бути в межах в межах [-10000, 10000].")
        if tolerance <= 0:
            raise MethodException("Точність має бути додатною.")
        if tolerance >= 10:
            raise MethodException("Точність має меншою за 10.")
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

        root = tk.Tk()
        root.resizable(False, False)
        root.title("Результат")
        root.geometry(f"+520+20")
        text = tk.Text(root, wrap="word", width=40)
        text.grid(column=0, row=0, sticky=tk.NSEW)

        ys = tk.Scrollbar(root, orient="vertical", command=text.yview)
        ys.grid(column=1, row=0, sticky=tk.NS)

        text["yscrollcommand"] = ys.set

        text.insert(tk.END, f"{self.equation} = 0\nМетод Ньютона:\n\n\n\n")
        try:
            while abs(self.function(x)) > self.tolerance and self.n_iterations < self.max_iterations:
                self.n_iterations += 1
                x = x - self.function(x) / self.derivative(x)
                text.configure(state="normal")
                text.insert(tk.END, f"Ітерація {self.n_iterations}\nx = {x}\n\n")
                text.configure(state="disabled")
        except Exception as e:
            text.configure(state="normal")
            text.insert("3.0", f"Помилка\n")
            text.insert("4.0", f"Ітерацій: {self.n_iterations}")
            text.insert(tk.END, f"Ітерація {self.n_iterations}\nПомилка")
            text.configure(state="disabled")
            raise e

        if abs(self.function(x)) <= self.tolerance:
            text.configure(state="normal")
            text.insert("3.0", f"x = {x}")
            text.insert("4.0", f"Ітерацій: {self.n_iterations}")
            text.configure(state="disabled")
            return x
        else:
            text.configure(state="normal")
            text.insert("3.0", f"Метод не збігся за {self.n_iterations} ітерацій.")
            text.configure(state="disabled")
            raise MethodException("Метод не збігся за вказану кількість ітерацій.")
