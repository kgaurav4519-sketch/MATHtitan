from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivymd.uix.button import MDRaisedButton, MDFillRoundFlatButton
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.gridlayout import GridLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.textfield import MDTextField 
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.core.clipboard import Clipboard
import sympy as sp
import matplotlib.pyplot as plt
import numpy as np
import re

# --- 1. TITAN TRANSLATOR (Human to Machine) ---
def titan_translator(text):
    # Power and Symbols
    text = text.replace('²', '**2').replace('³', '**3').replace('^', '**')
    text = text.replace('√', 'sqrt').replace('π', 'pi')
    # Fix implicit multiplication like 2x -> 2*x
    text = re.sub(r'(\d)([a-zA-Z\(])', r'\1*\2', text)
    return text

# --- 2. DISPLAY CLEANER (Machine to Human) ---
def titan_formatter(text):
    # Answer mein wapas ² aur ³ dikhane ke liye
    text = str(text).replace('**2', '²').replace('**3', '³')
    return text

# --- HOME SCREEN ---
class TitanHome(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = MDBoxLayout(orientation='vertical', spacing=20, padding=40)
        layout.add_widget(MDLabel(text="MATH TITAN", halign="center", font_style="H2", theme_text_color="Custom", text_color=(0.5, 0.2, 0.9, 1)))
        
        btns = [
            ("ARITHMETIC", "simple_calc", (0, 0.7, 0.9, 1)),
            ("CALCULUS PRO", "adv_math", (0.9, 0.1, 0.4, 1)),
            ("ALGEBRA & GRAPHING", "matrix_menu", (0.1, 0.8, 0.5, 1))
        ]
        
        for txt, target, col in btns:
            btn = MDFillRoundFlatButton(text=txt, font_size="20sp", pos_hint={"center_x": .5}, md_bg_color=col, size_hint_x=1)
            btn.bind(on_release=lambda x, t=target: self.change_screen(t))
            layout.add_widget(btn)
        self.add_widget(layout)
    def change_screen(self, t): self.manager.current = t

# --- ARITHMETIC SCREEN ---
class SimpleCalc(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = MDBoxLayout(orientation='vertical', padding=10, spacing=5)
        self.result = TextInput(font_size=50, halign='right', multiline=False, readonly=True, size_hint_y=0.2)
        layout.add_widget(self.result)
        grid = GridLayout(cols=4, spacing=5)
        for b in ['7','8','9','/','4','5','6','*','1','2','3','-','C','0','=','+']:
            grid.add_widget(Button(text=b, on_press=self.calculate))
        layout.add_widget(grid)
        layout.add_widget(MDRaisedButton(text="Back", on_release=lambda x: self.go_home(), pos_hint={"center_x":.5}))
        self.add_widget(layout)
    def calculate(self, instance):
        if instance.text == 'C': self.result.text = ""
        elif instance.text == '=':
            try: self.result.text = str(eval(self.result.text))
            except: self.result.text = "Error"
        else: self.result.text += instance.text
    def go_home(self): self.manager.current = "titan_home"

# --- CALCULUS SCREEN ---
class AdvMath(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = MDBoxLayout(orientation='vertical', spacing=10, padding=20)
        self.input = MDTextField(hint_text="Enter Equation (e.g., x² + sin(x))", mode="rectangle")
        self.res = TextInput(readonly=True, font_size=16, size_hint_y=0.4, background_color=(0,0,0,1), foreground_color=(1,1,1,1))
        layout.add_widget(self.input); layout.add_widget(self.res)
        
        # Shortcut bar
        bar = MDBoxLayout(spacing=5, size_hint_y=None, height="40dp")
        for s in ['x', '²', '√', 'sin(', 'π']:
            btn = MDRaisedButton(text=s, on_release=lambda x, sy=s: self.add_s(sy))
            bar.add_widget(btn)
        layout.add_widget(bar)
        
        row = GridLayout(cols=3, spacing=5, size_hint_y=None, height="50dp")
        row.add_widget(MDRaisedButton(text="Diff", on_release=self.diff))
        row.add_widget(MDRaisedButton(text="Steps", on_release=self.show_steps, md_bg_color=(1, 0.6, 0, 1)))
        row.add_widget(MDRaisedButton(text="Integ", on_release=self.integ))
        layout.add_widget(row)
        layout.add_widget(MDRaisedButton(text="Back", on_release=lambda x: self.go_home(), pos_hint={"center_x":.5}))
        self.add_widget(layout)

    def add_s(self, s): self.input.text += s
    def diff(self, _):
        try:
            ans = sp.diff(titan_translator(self.input.text), sp.Symbol('x'))
            self.res.text = f"Result:\n{titan_formatter(ans)}"
        except Exception as e: self.res.text = str(e)

    def show_steps(self, _):
        try:
            expr = titan_translator(self.input.text)
            ans = sp.diff(expr, sp.Symbol('x'))
            self.res.text = f"Problem: d/dx ({self.input.text})\nApplying rules...\nStep 1: Raw Derivative -> {ans}\nStep 2: Simplified -> {titan_formatter(sp.simplify(ans))}"
        except: self.res.text = "Error in Steps"

    def integ(self, _):
        try:
            ans = sp.integrate(titan_translator(self.input.text), sp.Symbol('x'))
            self.res.text = f"Integral:\n{titan_formatter(ans)} + C"
        except Exception as e: self.res.text = str(e)
    def go_home(self): self.manager.current = "titan_home"

# --- ALGEBRA & GRAPHING SCREEN ---
class MatrixMenu(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = MDBoxLayout(orientation='vertical', spacing=10, padding=20)
        self.input = MDTextField(hint_text="Equation (e.g., x² - 4)", mode="rectangle")
        self.res = TextInput(readonly=True, font_size=18, size_hint_y=0.4, background_color=(0,0,0,1), foreground_color=(0,1,0,1))
        layout.add_widget(self.input); layout.add_widget(self.res)
        
        btns = GridLayout(cols=2, spacing=10, size_hint_y=None, height="100dp")
        btns.add_widget(MDRaisedButton(text="Solve x", on_release=self.solve_eq))
        btns.add_widget(MDRaisedButton(text="Plot Graph", on_release=self.plot_graph, md_bg_color=(0.5, 0, 1, 1)))
        layout.add_widget(btns)
        layout.add_widget(MDRaisedButton(text="Back", on_release=lambda x: self.go_home(), pos_hint={"center_x": .5}))
        self.add_widget(layout)

    def solve_eq(self, _):
        try:
            sol = sp.solve(titan_translator(self.input.text), sp.Symbol('x'))
            self.res.text = f"Roots:\nx = {titan_formatter(sol)}"
        except Exception as e: self.res.text = str(e)

    def plot_graph(self, _):
        try:
            plt.clf()
            expr = titan_translator(self.input.text)
            f = sp.lambdify(sp.Symbol('x'), expr, "numpy")
            x = np.linspace(-10, 10, 400)
            y = f(x)
            plt.plot(x, y, color='purple', label=f"f(x)={self.input.text}")
            plt.axhline(0, color='black', lw=1); plt.axvline(0, color='black', lw=1)
            plt.grid(True, linestyle='--')
            plt.legend(); plt.title("Titan Graphing Engine")
            plt.show()
        except: self.res.text = "Graph Error: Use x as variable"
    def go_home(self): self.manager.current = "titan_home"

# --- MAIN APP ---
class MathTitan(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "DeepPurple"
        sm = ScreenManager(transition=FadeTransition())
        sm.add_widget(TitanHome(name="titan_home"))
        sm.add_widget(SimpleCalc(name="simple_calc"))
        sm.add_widget(AdvMath(name="adv_math"))
        sm.add_widget(MatrixMenu(name="matrix_menu"))
        return sm

if __name__ == "__main__":
    MathTitan().run()
