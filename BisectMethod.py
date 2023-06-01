import tkinter as tk
from numpy import *
from Method import *
from MethodException import *


class BisectMethod(Method):
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

    def b_solve(self):
        a = self.a
        b = self.b
        if self.function(a) * self.function(b) >= 0:
            raise MethodException("Значення функції в точках 'a' та 'b' мають мати різні знаки.")

        root = tk.Tk()
        root.resizable(False, False)
        root.title("Результат")
        root.geometry(f"+20+20")
        text = tk.Text(root, wrap="word", width=40)
        text.grid(column=0, row=0, sticky=tk.NSEW)

        ys = tk.Scrollbar(root, orient="vertical", command=text.yview)
        ys.grid(column=1, row=0, sticky=tk.NS)

        text["yscrollcommand"] = ys.set

        text.insert(tk.END, f"{self.equation} = 0\nМетод половинного ділення:\n\n\n\n")

        self.b_iterations = 0
        try:
            while abs(b - a) > self.tolerance:
                self.b_iterations += 1
                c = (a + b) / 2
                text.configure(state="normal")
                text.insert(tk.END, f"Ітерація {self.b_iterations}\nx = {c}\n\n")
                text.configure(state="disabled")
                if self.function(c) == 0:
                    text.configure(state="normal")
                    text.insert("3.0", f"x = {(a + b) / 2}")
                    text.insert("4.0", f"Ітерацій: {self.b_iterations}")
                    text.configure(state="disabled")
                    return c
                elif self.function(c) * self.function(a) < 0:
                    b = c
                else:
                    a = c
        except Exception as e:
            text.configure(state="normal")
            text.insert("3.0", f"Помилка")
            text.insert("4.0", f"Ітерацій: {self.b_iterations}")
            text.insert(tk.END, f"Ітерація {self.b_iterations}\nПомилка")
            text.configure(state="disabled")
            raise e
        text.configure(state="normal")
        text.insert("3.0", f"x = {(a + b) / 2}")
        text.insert("4.0", f"Ітерацій: {self.b_iterations}")
        text.configure(state="disabled")
        return (a + b) / 2
