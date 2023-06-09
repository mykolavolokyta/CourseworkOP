import tkinter as tk
from tkinter import filedialog
from Graphic import *
from Statistics import *


# Основний клас програми
class App(tk.Tk):
    # Конструктор
    def __init__(self):
        super().__init__()

        self.title("Калькулятор трансцендентних рівнянь")
        self.geometry(f"1000x620")
        self.resizable(False, False)
        self.COLOR = "#1bbce5"
        self.configure(bg=self.COLOR)

        self.a = tk.StringVar()
        self.a_entry = tk.Entry()
        self.b = tk.StringVar()
        self.b_entry = tk.Entry()
        self.e = tk.StringVar()
        self.e_entry = tk.Entry()
        self.initial_guess = tk.StringVar()
        self.initial_guess_entry = tk.Entry()
        self.max_iterations = tk.StringVar()
        self.max_iterations_entry = tk.Entry()
        tk.Label(self, text="Введіть рівняння: ", font=("Times New Roman", 12), bg=self.COLOR).grid(row=0, column=0, columnspan=2)
        self.equation = tk.StringVar()
        self.entry = tk.Entry(self, textvariable=self.equation, justify=tk.CENTER)
        self.entry.grid(row=1, column=0)
        tk.Label(self, text="=   0", font=("Times New Roman", 12), bg=self.COLOR).grid(row=1, column=1)
        tk.Button(self, text="Очистити", command=lambda: self.entry.delete(0, tk.END), width=20).grid(row=2, column=0, columnspan=2)
        tk.Label(self, text="Вибір алгоритму: ", font=("Times New Roman", 12), pady=10, bg=self.COLOR).grid(row=3, column=0, columnspan=2)
        self.method = tk.StringVar(value="bisect")
        tk.Radiobutton(self, text="Метод половинного ділення", font=("Times New Roman", 12), bg=self.COLOR, value="bisect", variable=self.method, command=self.make_bisect_frame, padx=20).grid(row=4, column=0, columnspan=2, sticky='w')
        tk.Radiobutton(self, text="Метод дотичних(Ньютона)", font=("Times New Roman", 12), bg=self.COLOR, value="newton", variable=self.method, command=self.make_newton_frame, padx=20).grid(row=5, column=0, columnspan=2, sticky='w')
        tk.Radiobutton(self, text="Метод січних", value="secant", font=("Times New Roman", 12), bg=self.COLOR, variable=self.method, command=self.make_secant_frame, padx=20).grid(row=6, column=0, columnspan=2, sticky='w')

        self.method_frame = tk.Frame(self, bg=self.COLOR)
        self.make_bisect_frame()
        self.method_frame.grid(row=7, column=0, columnspan=2, sticky='w', padx=30)

        tk.Label(self, text="", font=("Times New Roman", 12), bg=self.COLOR).grid(row=8, column=0, columnspan=2)
        tk.Button(self, text="Обчислити", command=self.solve, width=30, height=3).grid(row=9, column=0, columnspan=2)
        tk.Label(self, text="", font=("Times New Roman", 1), bg=self.COLOR).grid(row=10, column=0, columnspan=2)
        tk.Button(self, text="Побудувати графік", command=self.print_graphic, width=30, height=3).grid(row=11, column=0, columnspan=2)

        tk.Label(self, text="Хід розв'язку", font=("Times New Roman", 12), bg=self.COLOR, padx=50).grid(row=0, column=2)
        self.solution = tk.Text(self, font=("Times New Roman", 12), state="disabled", width=30, height=30)
        self.solution.grid(row=1, column=2, rowspan=20, sticky="n")

        ys = tk.Scrollbar(orient="vertical", command=self.solution.yview)
        ys.grid(row=1, column=2, rowspan=20, sticky="nse")
        self.solution["yscrollcommand"] = ys.set

        tk.Label(self, text="", font=("Times New Roman", 12), bg=self.COLOR, padx=15).grid(row=0, column=3)
        tk.Label(self, text="Результат", font=("Times New Roman", 12), bg=self.COLOR).grid(row=0, column=4, columnspan=2)
        tk.Label(self, text="X =", font=("Times New Roman", 14), bg=self.COLOR).grid(row=1, column=4, sticky='e')
        self.result = tk.Entry(self, font=("Times New Roman", 12), justify=tk.CENTER, width=20, state="readonly")
        self.result.grid(row=1, column=5, sticky='w')

        tk.Label(self, text="", font=("Times New Roman", 12), bg=self.COLOR, pady=1).grid(row=2, column=3, columnspan=2)
        tk.Button(self, text="Аналітика", command=self.analyze, width=10).grid(row=3, column=4)
        tk.Button(self, text="Зберегти в файл", command=self.save_to_file, width=15).grid(row=3, column=5)
        tk.Label(self, text="", font=("Times New Roman", 12), bg=self.COLOR, pady=2).grid(row=4, column=3, columnspan=2)

        tk.Label(self, text="Графік", font=("Times New Roman", 12), bg=self.COLOR).grid(row=5, column=4, columnspan=2)

        self.statistics = None
        self.graphic = Graphic("")
        self.graphic.chart.get_tk_widget().grid(row=6, column=4, columnspan=2, rowspan=8, sticky='n')

    # Метод для створення віджета, що містить параметри, необхідні для методу половинного ділення
    def make_bisect_frame(self):
        for widget in self.method_frame.winfo_children():
            widget.destroy()

        tk.Label(self.method_frame, text="Введіть межі пошуку кореня: ", font=("Times New Roman", 12), bg=self.COLOR, pady=10).grid(row=0, column=0, columnspan=20)
        tk.Label(self.method_frame, text="a =", font=("Times New Roman", 12), bg=self.COLOR, width=3).grid(row=1, column=0, sticky='w')
        self.a_entry = tk.Entry(self.method_frame, textvariable=self.a, justify=tk.CENTER, width=5)
        self.a_entry.grid(row=1, column=1, sticky='w')
        tk.Label(self.method_frame, text="b =", font=("Times New Roman", 12), bg=self.COLOR).grid(row=1, column=7, sticky='w')
        self.b_entry = tk.Entry(self.method_frame, textvariable=self.b, justify=tk.CENTER, width=5)
        self.b_entry.grid(row=1, column=8, sticky='w')
        tk.Label(self.method_frame, text="Введіть точність: ", font=("Times New Roman", 12), bg=self.COLOR, pady=10).grid(row=2, column=0, columnspan=10)
        tk.Label(self.method_frame, text="e =", font=("Times New Roman", 12), bg=self.COLOR).grid(row=3, column=2, sticky='w')
        self.e_entry = tk.Entry(self.method_frame, textvariable=self.e, justify=tk.CENTER, width=10)
        self.e_entry.grid(row=3, column=3, sticky='w')
        tk.Button(self.method_frame, text="Очистити", command=self.delete_bisect, width=30).grid(row=4, column=0, columnspan=20)

    # Метод для створення віджета, що містить параметри, необхідні для методу Ньютона
    def make_newton_frame(self):
        for widget in self.method_frame.winfo_children():
            widget.destroy()
        tk.Label(self.method_frame, text="Введіть початкове припущення: ", font=("Times New Roman", 12), bg=self.COLOR, pady=10).grid(row=0, column=0, columnspan=2)
        tk.Label(self.method_frame, text="x =", font=("Times New Roman", 12), bg=self.COLOR).grid(row=1, column=0, sticky='e')
        self.initial_guess_entry = tk.Entry(self.method_frame, textvariable=self.initial_guess, justify=tk.CENTER, width=10)
        self.initial_guess_entry.grid(row=1, column=1, sticky='w')
        tk.Label(self.method_frame, text="Введіть точність: ", font=("Times New Roman", 12), bg=self.COLOR, pady=10).grid(row=2, column=0, columnspan=2)
        tk.Label(self.method_frame, text="e =", font=("Times New Roman", 12), bg=self.COLOR).grid(row=3, column=0, sticky='e')
        self.e_entry = tk.Entry(self.method_frame, textvariable=self.e, justify=tk.CENTER, width=10)
        self.e_entry.grid(row=3, column=1, sticky='w')
        tk.Label(self.method_frame, text="Введіть кількість ітерацій: ", font=("Times New Roman", 12), bg=self.COLOR, pady=10).grid(row=4, column=0, columnspan=2)
        tk.Label(self.method_frame, text="n =", font=("Times New Roman", 12), bg=self.COLOR).grid(row=5, column=0, sticky='e')
        self.max_iterations_entry = tk.Entry(self.method_frame, textvariable=self.max_iterations, justify=tk.CENTER, width=10)
        self.max_iterations_entry.grid(row=5, column=1, sticky='w')
        tk.Button(self.method_frame, text="Очистити", command=self.delete_newton, width=30).grid(row=6, column=0, columnspan=2)

    # Метод для створення віджета, що містить параметри, необхідні для методу січних
    def make_secant_frame(self):
        for widget in self.method_frame.winfo_children():
            widget.destroy()
        tk.Label(self.method_frame, text="Введіть межі пошуку кореня: ", font=("Times New Roman", 12), bg=self.COLOR, pady=10).grid(row=0, column=0, columnspan=20)
        tk.Label(self.method_frame, text="a =", font=("Times New Roman", 12), bg=self.COLOR, width=3).grid(row=1, column=0, sticky='w')
        self.a_entry = tk.Entry(self.method_frame, textvariable=self.a, justify=tk.CENTER, width=5)
        self.a_entry.grid(row=1, column=1, sticky='w')
        tk.Label(self.method_frame, text="b =", font=("Times New Roman", 12), bg=self.COLOR).grid(row=1, column=7, sticky='w')
        self.b_entry = tk.Entry(self.method_frame, textvariable=self.b, justify=tk.CENTER, width=5)
        self.b_entry.grid(row=1, column=8, sticky='w')
        tk.Label(self.method_frame, text="Введіть точність: ", font=("Times New Roman", 12), bg=self.COLOR, pady=10).grid(row=2, column=0, columnspan=10)
        tk.Label(self.method_frame, text="e =", font=("Times New Roman", 12), bg=self.COLOR).grid(row=3, column=2, sticky='w')
        self.e_entry = tk.Entry(self.method_frame, textvariable=self.e, justify=tk.CENTER, width=10)
        self.e_entry.grid(row=3, column=3, sticky='w')
        tk.Label(self.method_frame, text="Введіть кількість ітерацій: ", font=("Times New Roman", 12), bg=self.COLOR, pady=10).grid(row=4, column=0, columnspan=10)
        tk.Label(self.method_frame, text="n =", font=("Times New Roman", 12), bg=self.COLOR).grid(row=5, column=2, sticky='w')
        self.max_iterations_entry = tk.Entry(self.method_frame, textvariable=self.max_iterations, justify=tk.CENTER, width=10)
        self.max_iterations_entry.grid(row=5, column=3, sticky='w')
        tk.Button(self.method_frame, text="Очистити", command=self.delete_secant, width=30).grid(row=6, column=0, columnspan=20)

    # Очищення полів параметрів, необхідних для методу половинного ділення
    def delete_bisect(self):
        self.a_entry.delete(0, tk.END)
        self.b_entry.delete(0, tk.END)
        self.e_entry.delete(0, tk.END)

    # Очищення полів параметрів, необхідних для методу Ньютона
    def delete_newton(self):
        self.initial_guess_entry.delete(0, tk.END)
        self.e_entry.delete(0, tk.END)
        self.max_iterations_entry.delete(0, tk.END)

    # Очищення полів параметрів, необхідних для методу січних
    def delete_secant(self):
        self.a_entry.delete(0, tk.END)
        self.b_entry.delete(0, tk.END)
        self.e_entry.delete(0, tk.END)
        self.max_iterations_entry.delete(0, tk.END)

    # Метод для обчислення трансцендентного рівняння обраним методом
    def solve(self):
        try:
            self.equation.set(self.equation.get().replace("^", "**"))
            if self.method.get() == "bisect":
                self.solve_bisect()
            if self.method.get() == "newton":
                self.solve_newton()
            if self.method.get() == "secant":
                self.solve_secant()
            return True
        except ZeroDivisionError:
            showwarning("Помилка", "Ділення на 0.")
        except FloatingPointError:
            showwarning("Помилка", "Неприпустиме значення.")
        except (NameError, SyntaxError):
            showwarning("Помилка", "Некоректний ввід.")
        except ValueError:
            showwarning("Помилка", "Заповніть всі поля коректно.")
        except MethodException as e:
            showwarning("Помилка", e)
        except OverflowError:
            showwarning("Помилка", "Задано завеликі значення")
        return False

    # Метод для обчислення трансцендентного рівняння методом половинного ділення
    def solve_bisect(self):
        bisect = BisectMethod(self.equation.get(), float(self.a.get()), float(self.b.get()), float(self.e.get()))
        result = bisect.b_solve(self.solution)
        self.result.configure(state="normal")
        self.result.delete(0, tk.END)
        self.result.insert(0, result)
        self.result.configure(state="readonly")

    # Метод для обчислення трансцендентного рівняння методом Ньютона
    def solve_newton(self):
        newton = NewtonMethod(self.equation.get(), float(self.initial_guess.get()), float(self.e.get()), int(self.max_iterations.get()))
        result = newton.n_solve(self.solution)
        self.result.configure(state="normal")
        self.result.delete(0, tk.END)
        self.result.insert(0, result)
        self.result.configure(state="readonly")

    # Метод для обчислення трансцендентного рівняння методом січних
    def solve_secant(self):
        secant = SecantMethod(self.equation.get(), float(self.a.get()), float(self.b.get()), float(self.e.get()), int(self.max_iterations.get()))
        result = secant.s_solve(self.solution)
        self.result.configure(state="normal")
        self.result.delete(0, tk.END)
        self.result.insert(0, result)
        self.result.configure(state="readonly")

    # Метод для виведення статистичних даних (кількість ітерацій) для кожного алгоритму
    def analyze(self):
        try:
            self.statistics = Statistics(self.equation.get(), float(self.a.get()), float(self.b.get()), float(self.e.get()), float(self.initial_guess.get()), int(self.max_iterations.get()))
            self.statistics.get_statistics()
        except ZeroDivisionError:
            showwarning("Помилка", "Ділення на 0.")
        except (NameError, SyntaxError):
            showwarning("Помилка", "Некоректний ввід.")
        except ValueError:
            showwarning("Помилка", "Заповніть всі поля коректно.")
        except FloatingPointError:
            showwarning("Помилка", "Неприпустиме значення.")
        except MethodException as e:
            showwarning("Помилка", e)
        except OverflowError:
            showwarning("Помилка", "Задано завеликі значення")

    # Метод для виведення збереження результату розв'язку в файл
    def save_to_file(self):
        try:
            if self.solve():
                result = self.equation.get() + " = 0   =>   x = " + str(self.result.get())
                filepath = filedialog.asksaveasfilename()
                if filepath != "":
                    with open(filepath, "w") as file:
                        file.write(result)
                    showinfo("Перемога", "Збережено до файлу.")
        except OSError:
            showwarning("Помилка", "Помилка при відкритті файла")

    # Метод для побудови графіку трансцендентного рівняння
    def print_graphic(self):
        try:
            plt.close(self.graphic.figure)
            self.graphic = Graphic(self.equation.get())
            self.graphic.chart.get_tk_widget().grid(row=6, column=4, columnspan=2, rowspan=8, sticky='n')
        except (NameError, SyntaxError):
            showwarning("Помилка", "Некоректний ввід.")
        except OverflowError:
            showwarning("Помилка", "Задано завеликі значення")