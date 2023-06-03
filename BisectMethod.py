import tkinter as tk
from numpy import *
from Method import *
from MethodException import *


# Клас, який представляє метод половинного ділення
class BisectMethod(Method):
    # Конструктор
    def __init__(self, equation, a, b, tolerance):
        if a >= b:
            raise MethodException("'a' має бути менше за 'b'.")
        if a < -10000 or b > 10000:
            raise MethodException("'a' та 'b' мають бути в межах [-10000, 10000].")
        if tolerance <= 0:
            raise MethodException("Точність має бути додатною.")
        if tolerance >= 10:
            raise MethodException("Точність має меншою за 10.")
        Method.__init__(self, equation)
        self.a = a
        self.b = b
        self.tolerance = tolerance
        self.b_iterations = 0

    # Метод для розв'язку рівняння методом половинного ділення
    # Якщо в метод передається параметр widget, то в нього записується хід розв'язку
    def b_solve(self, widget=None):
        a = self.a
        b = self.b
        if self.function(a) * self.function(b) >= 0:
            raise MethodException("Значення функції в точках 'a' та 'b' мають мати різні знаки.")

        if widget:
            widget.configure(state="normal")
            widget.delete("1.0", tk.END)
            widget.insert(tk.END, f"{self.equation} = 0\nМетод половинного ділення:\n\n\n\n")
            widget.configure(state="disabled")

        self.b_iterations = 0
        try:
            while abs(b - a) > self.tolerance:
                self.b_iterations += 1
                c = (a + b) / 2
                if widget:
                    widget.configure(state="normal")
                    widget.insert(tk.END, f"Ітерація {self.b_iterations}\nx = {c}\n\n")
                    widget.configure(state="disabled")
                if self.function(c) == 0:
                    if widget:
                        widget.configure(state="normal")
                        widget.insert("3.0", f"x = {(a + b) / 2}")
                        widget.insert("4.0", f"Ітерацій: {self.b_iterations}")
                        widget.configure(state="disabled")
                    return c
                elif self.function(c) * self.function(a) < 0:
                    b = c
                else:
                    a = c
        except Exception as e:
            if widget:
                widget.configure(state="normal")
                widget.insert("3.0", f"Помилка")
                widget.insert("4.0", f"Ітерацій: {self.b_iterations}")
                widget.insert(tk.END, f"Ітерація {self.b_iterations}\nПомилка")
                widget.configure(state="disabled")
            raise e
        if widget:
            widget.configure(state="normal")
            widget.insert("3.0", f"x = {(a + b) / 2}")
            widget.insert("4.0", f"Ітерацій: {self.b_iterations}")
            widget.configure(state="disabled")
        return (a + b) / 2
