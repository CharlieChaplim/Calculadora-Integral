import tkinter as tk
from tkinter import ttk
import sympy as sp
import re

class IntegralCalculatorApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Calculadora Integral")
        self.geometry("420x400")
        self.resizable(False, False)
        self.create_widgets()

    def create_widgets(self):
        # Label "Entrada" no topo
        self.label_input = ttk.Label(self, text="Entrada", font=("Arial", 14))
        self.label_input.pack(pady=(20, 5))

        # Campo de entrada para o usuário digitar a função
        self.input_entry = ttk.Entry(self, font=("Arial", 12), justify="center")
        self.input_entry.pack(fill="x", padx=60, pady=(0, 10))

        # Mini teclado de símbolos
        self.create_symbol_keyboard()

        # Frame dos botões
        button_frame = ttk.Frame(self)
        button_frame.pack(pady=(10, 15))

        # Botão "Derivar"
        self.btn_derive = ttk.Button(button_frame, text="Derivar", command=self.derive)
        self.btn_derive.pack(side="left", padx=10)

        # Botão "Integrar"
        self.btn_integrate = ttk.Button(button_frame, text="Integrar", command=self.integrate)
        self.btn_integrate.pack(side="left", padx=10)

        # Campo de saída
        self.output_entry = ttk.Entry(self, font=("Arial", 12), justify="center")
        self.output_entry.pack(fill="x", padx=60, pady=(0, 5))

        # Label "Saída"
        self.label_output = ttk.Label(self, text="Saída", font=("Arial", 14))
        self.label_output.pack(pady=(5, 0))

    # Função para criar o teclado de símbolos
    def create_symbol_keyboard(self):
        symbol_frame = ttk.Frame(self)
        symbol_frame.pack(pady=(0, 10))

        symbols = [
            ("√", "√("), ("^", "^"), ("²", "²"), ("³", "³"),
            ("π", "pi"), ("e", "e"),
            ("sen", "sen("), ("cos", "cos("), ("tan", "tan("),
            ("ln", "ln("), ("log", "log("),
            ("(", "("), (")", ")"), ("x", "x")
        ]

        for i, (label, insert_text) in enumerate(symbols):
            btn = ttk.Button(symbol_frame, text=label, width=4,
                             command=lambda txt=insert_text: self.insert_symbol(txt))
            btn.grid(row=i // 6, column=i % 6, padx=2, pady=2)

    def insert_symbol(self, text):
        self.input_entry.insert(tk.END, text)

    def parse_input(self, user_input):
        # Substituições para tornar a entrada compatível com sympy
        user_input = user_input.replace("^", "**")
        user_input = user_input.replace("²", "**2")
        user_input = user_input.replace("³", "**3")
        user_input = user_input.replace("√", "sqrt")
        user_input = user_input.replace("sen", "sin")
        user_input = user_input.replace("ln", "log")
        return sp.sympify(user_input)

    def format_output_readable(self, expr):
        text = str(expr)

        # Raiz quadrada
        text = re.sub(r'sqrt\((.*?)\)', r'√(\1)', text)

        # Potências específicas
        text = text.replace("**2", "²").replace("**3", "³")

        # Potências genéricas
        text = re.sub(r'\*\*(\d+)', r'^\1', text)

        # Multiplicação implícita
        text = text.replace("*", "")

        # Funções
        text = text.replace("sin", "sen")
        text = text.replace("log", "ln")
        text = text.replace("pi", "π")

        return text

    # Função de derivada
    def derive(self):
        func_str = self.input_entry.get()
        x = sp.symbols('x')
        try:
            func = self.parse_input(func_str)
            first_derivative = sp.diff(func, x)
            second_derivative = sp.diff(func, x, 2)
            result = (
                f"1ª derivada: {self.format_output_readable(sp.simplify(first_derivative))} | "
                f"2ª derivada: {self.format_output_readable(sp.simplify(second_derivative))}"
            )
        except Exception as e:
            result = f"Erro: {e}"

        self.output_entry.delete(0, tk.END)
        self.output_entry.insert(0, result)

    #Função de integral
    def integrate(self):
        func_str = self.input_entry.get()
        x = sp.symbols('x')
        try:
            func = self.parse_input(func_str)
            integral = sp.integrate(func, x)
            result = f"Integral indefinida: {self.format_output_readable(sp.simplify(integral))} + C"
        except Exception as e:
            result = f"Erro: {e}"

        self.output_entry.delete(0, tk.END)
        self.output_entry.insert(0, result)

# Execução principal
if __name__ == "__main__":
    app = IntegralCalculatorApp()
    app.mainloop()
