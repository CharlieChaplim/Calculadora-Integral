import tkinter as tk
import sympy as sp
import re
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from customtkinter import *

plt.rcParams.update({
    "text.usetex":True,
})
set_appearance_mode("light")
WHITE_COLOR = "#ebebeb"

class IntegralCalculatorApp(CTk):
    def __init__(self):
        self.fig, self.ax = plt.subplots()
        self.ax.axis("off")
        super().__init__()
        self.title("Calculadora Integral")
        self.geometry("420x400")
        self.resizable(False, False)
        self.create_widgets()

    def create_widgets(self):
        # Label "Entrada" no topo
        self.label_input = CTkLabel(self, text="Entrada", font=("Arial", 14))
        self.label_input.pack(pady=(20, 5))

        # Campo de entrada para o usuário digitar a função
        self.input_entry = CTkEntry(self, font=("Arial", 12), justify="center")
        self.input_entry.pack(fill="x", padx=60, pady=(0, 10))

        # Mini teclado de símbolos
        self.create_symbol_keyboard()

        # Frame dos botões
        button_frame = CTkFrame(self, bg_color=WHITE_COLOR, fg_color=WHITE_COLOR)
        button_frame.pack(pady=(10, 15))

        # Botão "Derivar"
        self.btn_derive = CTkButton(button_frame, text="Derivar", command=self.derive)
        self.btn_derive.pack(side="left", padx=10)

        # Botão "Integrar"
        self.btn_integrate = CTkButton(button_frame, text="Integrar", command=self.integrate)
        self.btn_integrate.pack(side="left", padx=10)

        # Label "Saída"
        self.label_output = CTkLabel(self, text="Saída", font=("Arial", 14))
        self.label_output.pack(pady=(0, 0))

        # Campo de saída
        # self.output_entry = CTkTextbox(  self, font=("Arial", 12))
        # self.output_entry.pack(pady=(10, 50))

        self.output_canvas = FigureCanvasTkAgg(self.fig, self)
        self.output_widget = self.output_canvas.get_tk_widget()
        self.output_widget.configure(height=200,width=300)
        self.output_widget.pack()


    # Função para criar o teclado de símbolos
    def create_symbol_keyboard(self):
        symbol_frame = CTkFrame(self, fg_color=WHITE_COLOR)
        symbol_frame.pack(pady=(0, 10))

        symbols = [
            ("√", "√("), ("^", "^"), ("²", "²"), ("³", "³"),
            ("π", "pi"), ("e", "e"),
            ("sen", "sen("), ("cos", "cos("), ("tan", "tan("),
            ("ln", "ln("), ("log", "log("),
            ("(", "("), (")", ")"), ("x", "x")
        ]

        for i, (label, insert_text) in enumerate(symbols):
            btn = CTkButton(symbol_frame, text=label, width=50,
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
            self.update_plot(f"1º Ordem:${sp.latex(sp.simplify(first_derivative))}$\n2º Ordem:${sp.latex(sp.simplify(second_derivative))}$", 20)
            result = (
                f"1ª derivada: {self.format_output_readable(sp.simplify(first_derivative))} \n" +
                f"2ª derivada: {self.format_output_readable(sp.simplify(second_derivative))}"
            )
        except Exception as e:
            result = f"Erro: {e}"
        
        print(result)
        self.output_canvas.draw()

    #Função de integral
    def integrate(self):
        self.output_widget.delete(ALL)

        func_str = self.input_entry.get()
        x = sp.symbols('x')
        try:
            func = self.parse_input(func_str)
            integral = sp.integrate(func, x)
            self.update_plot(f"${sp.latex(sp.simplify(integral))}$")
            
            result = f"Integral indefinida: {sp.latex(sp.simplify(integral))} + C"
        except Exception as e:
            result = f"Erro: {e}"
        
        print(result)

        self.output_canvas.draw()

    # Destroi e recria o canvas de resposta com uma nova equação
    def update_plot(self, new_text, font_size=25):
        self.output_widget.destroy()
        self.output_widget = None
        self.output_canvas = None

        self.fig, self.ax = plt.subplots()
        self.ax.axis("off")

        self.output_canvas = FigureCanvasTkAgg(self.fig, self)
        self.output_widget = self.output_canvas.get_tk_widget()
        self.output_widget.configure(height=200,width=300, bg="black")
        self.output_widget.pack()

        self.ax.text(-0.1,0.1, new_text, fontsize=font_size)

# Execução principal
if __name__ == "__main__":
    app = IntegralCalculatorApp()
    app.mainloop()
    plt.close("all")
