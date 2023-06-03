import tkinter as tk
from numpy import *
from Method import *
from MethodException import *


# Клас, який представляє метод січних
class SecantMethod(Method):
    # Конструктор
    def __init__(self, equation, a, b, tolerance, max_iterations):
        if a >= b:
            raise MethodException("'a' має бути менше за 'b'.")
        if a < -10000 or b > 10000:
            raise MethodException("'a' та 'b' мають бути в межах [-10000, 10000].")
        if tolerance <= 0:
            raise MethodException("Точність має бути додатною.")
        if tolerance >= 10:
            raise MethodException("Точність має меншою за 10.")
        if max_iterations <= 0:
            raise MethodException("Кількість ітерацій має бути додатною.")
        if max_iterations > 1000000:
            raise MethodException("Кількість ітерацій має бути меншою за 1000000.")
        Method.__init__(self, equation)
        self.a = a
        self.b = b
        self.tolerance = tolerance
        self.max_iterations = max_iterations
        self.s_iterations = 0

    # Метод для розв'язку рівняння методом січних
    # Якщо в метод передається параметр widget, то в нього записується хід розв'язку
    def s_solve(self, widget=None):
        if self.function(self.a) * self.function(self.b) >= 0:
            raise MethodException("Значення функції в точках 'a' та 'b' мають мати різні знаки.")

        x0 = self.a
        x1 = self.b
        self.s_iterations = 0

        if widget:
            widget.configure(state="normal")
            widget.delete("1.0", tk.END)
            widget.insert(tk.END, f"{self.equation} = 0\nМетод січних:\n\n\n\n")
            widget.configure(state="disabled")

        try:
            while abs(self.function(x1)) > self.tolerance and self.s_iterations < self.max_iterations:
                self.s_iterations += 1
                x2 = x1 - (self.function(x1) * (x1 - x0)) / (self.function(x1) - self.function(x0))
                x0 = x1
                x1 = x2
                if widget:
                    widget.configure(state="normal")
                    widget.insert(tk.END, f"Ітерація {self.s_iterations}\nx = {x1}\n\n")
                    widget.configure(state="disabled")
        except Exception as e:
            if widget:
                widget.configure(state="normal")
                widget.insert("3.0", f"Помилка\n")
                widget.insert("4.0", f"Ітерацій: {self.s_iterations}")
                widget.insert(tk.END, f"Ітерація {self.s_iterations}\nПомилка")
                widget.configure(state="disabled")
            raise e

        if abs(self.function(x1)) <= self.tolerance:
            if widget:
                widget.configure(state="normal")
                widget.insert("3.0", f"x = {x1}")
                widget.insert("4.0", f"Ітерацій: {self.s_iterations}")
                widget.configure(state="disabled")
            return x1
        else:
            if widget:
                widget.configure(state="normal")
                widget.insert("3.0", f"Метод не збігся за {self.s_iterations} ітерацій.")
                widget.configure(state="disabled")
            raise MethodException("Метод січних не збігся за вказану кількість ітерацій.")
