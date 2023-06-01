import tkinter as tk
from numpy import *
from Method import *
from MethodException import *


class SecantMethod(Method):
    def __init__(self, equation, a, b, tolerance, max_iterations):
        if a >= b:
            raise MethodException("'a' має бути менше за 'b'.")
        if a < -10000 or b > 10000:
            raise MethodException("'a' та 'b' мають бути в межах [-10000, 10000].")
        if tolerance <= 0:
            raise MethodException("Точність має бути додатною.")
        if max_iterations <= 0:
            raise MethodException("Кількість ітерацій має бути додатною.")
        if tolerance >= 10:
            raise MethodException("Точність має меншою за 10.")
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

        root = tk.Tk()
        root.resizable(False, False)
        root.title("Результат")
        root.geometry(f"+1020+20")
        text = tk.Text(root, wrap="word", width=40)
        text.grid(column=0, row=0, sticky=tk.NSEW)

        ys = tk.Scrollbar(root, orient="vertical", command=text.yview)
        ys.grid(column=1, row=0, sticky=tk.NS)

        text["yscrollcommand"] = ys.set

        text.insert(tk.END, f"{self.equation} = 0\nМетод січних:\n\n\n\n")
        try:
            while abs(self.function(x1)) > self.tolerance and self.s_iterations < self.max_iterations:
                self.s_iterations += 1
                x2 = x1 - (self.function(x1) * (x1 - x0)) / (self.function(x1) - self.function(x0))
                x0 = x1
                x1 = x2
                text.configure(state="normal")
                text.insert(tk.END, f"Ітерація {self.s_iterations}\nx = {x1}\n\n")
                text.configure(state="disabled")
        except Exception as e:
            text.configure(state="normal")
            text.insert("3.0", f"Помилка\n")
            text.insert("4.0", f"Ітерацій: {self.s_iterations}")
            text.insert(tk.END, f"Ітерація {self.s_iterations}\nПомилка")
            text.configure(state="disabled")
            raise e

        if abs(self.function(x1)) <= self.tolerance:
            text.configure(state="normal")
            text.insert("3.0", f"x = {x1}")
            text.insert("4.0", f"Ітерацій: {self.s_iterations}")
            text.configure(state="disabled")
            return x1
        else:
            text.configure(state="normal")
            text.insert("3.0", f"Метод не збігся за {self.s_iterations} ітерацій.")
            text.configure(state="disabled")
            raise MethodException("Метод не збігся за вказану кількість ітерацій.")
