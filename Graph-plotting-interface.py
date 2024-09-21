import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import sympy as sp
import numpy as np

class GraphingCalculatorApp:
    def __init__(self, master):
        self.master = master
        self.master.title("3D Graphing Calculator")

        ttk.Label(master, text="Equation in terms of x and y:").grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.equation_entry = ttk.Entry(master, width=30)
        self.equation_entry.grid(row=0, column=1, padx=10, pady=10, sticky="w")

        self.fig = plt.Figure(figsize=(8, 6), tight_layout=True)
        self.ax = self.fig.add_subplot(111, projection='3d')
        self.canvas = FigureCanvasTkAgg(self.fig, master=master)
        self.canvas.get_tk_widget().grid(row=1, column=0, columnspan=2, padx=10, pady=10)

        ttk.Button(master, text="Plot Graph", command=self.plot_graph).grid(row=2, column=0, padx=10, pady=10)

        self.sets = [
            ['QM', 'Calculus', 'Pure Math', 'Algebra'],
            ['Set 1', 'Set 2', 'Set 3', 'Set 4']
        ]
        self.current_set = tk.StringVar(value=self.sets[0][0])

        for i, set_name in enumerate(self.sets[0]):
            ttk.Button(master, text=set_name, command=lambda s=set_name: self.show_set_symbols(s)).grid(row=2, column=i+1, padx=5, pady=5)

        calculator_buttons = [
            ['7', '8', '9', 'y'],
            ['4', '5', '6', 'x'],
            ['1', '2', '3', '='],
            ['0', '.', '∫', '∑']
        ]

        for i, row in enumerate(calculator_buttons):
            for j, button in enumerate(row):
                ttk.Button(master, text=button, command=lambda b=button: self.insert_symbol(b)).grid(row=i+3, column=j, padx=5, pady=5)

    def plot_graph(self):
        equation_str = self.equation_entry.get()
        lhs, rhs = equation_str.split('=')
        x, y = sp.symbols('x y')
        equation = sp.sympify(rhs, evaluate=False)
        self.ax.clear()
        x_vals = np.linspace(-5, 5, 100)
        y_vals = np.linspace(-5, 5, 100)
        X, Y = np.meshgrid(x_vals, y_vals)
        func = sp.lambdify((x, y), equation, 'numpy')
        Z = func(X, Y)
        self.ax.plot_surface(X, Y, Z, cmap='viridis', edgecolor='k')
        self.canvas.draw()

    def insert_symbol(self, symbol):
        current_text = self.equation_entry.get()
        cursor_index = self.equation_entry.index(tk.INSERT)
        if symbol == '=':
            if cursor_index > 0 and current_text[cursor_index - 1] == '=':
                new_text = current_text[:cursor_index - 1] + '= ' + current_text[cursor_index:]
            else:
                new_text = current_text[:cursor_index] + '= ' + current_text[cursor_index:]
        else:
            new_text = current_text[:cursor_index] + f"{symbol} " + current_text[cursor_index:]
        self.equation_entry.delete(0, tk.END)
        self.equation_entry.insert(0, new_text)

    def show_set_symbols(self, symbol_set):
        set_symbols = self.get_set_symbols(symbol_set)
        set_window = tk.Toplevel(self.master)
        set_window.title(f"{symbol_set} Symbols")
        for i, row in enumerate(set_symbols):
            for j, symbol in enumerate(row):
                ttk.Button(set_window, text=symbol, command=lambda s=symbol: self.insert_symbol(s)).grid(row=i, column=j, padx=5, pady=5)

    def get_set_symbols(self, symbol_set):
        if symbol_set == 'QM':
            return [['∫', '∑', '∞'], ['∬', '∭', '∮'], ['∇', '∂', 'Ψ']]
        elif symbol_set == 'Calculus':
            return [['∫', '∑', '∞'], ['∬', '∭', '∮'], ['∇', '∂', 'ƒ']]
        elif symbol_set == 'Pure Math':
            return [['α', 'β', 'γ'], ['Δ', 'Ω', 'Σ'], ['π', 'ρ', 'σ']]
        elif symbol_set == 'Algebra':
            return [['⊕', '⊗', '⊖'], ['∀', '∈', '∧'], ['⇒', '⇔', '≡']]
        else:
            return [[]]

if __name__ == "__main__":
    root = tk.Tk()
    app = GraphingCalculatorApp(root)
    root.mainloop()
