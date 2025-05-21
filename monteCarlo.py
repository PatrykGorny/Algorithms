import tkinter as tk
from tkinter import ttk
import math
import random


def configure_style(window):
    style = ttk.Style()
    style.theme_use('clam')

    bg_color = '#121212'
    frame_bg = '#1E1E1E'
    button_bg = '#2D2D2D'
    button_active = '#3D3D3D'
    text_color = '#FFFFFF'
    entry_bg = '#252526'
    border_color = '#333333'

    window.configure(bg=bg_color)

    default_font = ('Segoe UI', 10)
    title_font = ('Segoe UI', 11, 'bold')

    style.configure('TFrame', background=bg_color)
    style.configure('TLabel', background=bg_color, foreground=text_color, font=default_font)
    style.configure('TLabelframe', background=bg_color, foreground=text_color, relief='flat', borderwidth=1)
    style.configure('TLabelframe.Label', font=title_font, background=bg_color, foreground=text_color)
    style.configure('Result.TLabel', background=bg_color, foreground=text_color, font=title_font, relief='flat',
                    borderwidth=0)
    style.configure('RoundButton.TButton', background=button_bg, foreground=text_color, borderwidth=0, relief='flat',
                    font=default_font, padding=8)
    style.map('RoundButton.TButton', background=[('active', button_active), ('pressed', button_bg)],
              foreground=[('active', text_color), ('pressed', text_color)])

    return entry_bg, text_color


def f(x):
    return abs(math.sin(x) + math.sin(2 * x) + math.sin(4 * x) + math.sin(8 * x))


def calculate_surface_monte_carlo(num_samples=1000000, a=0, b=2 * math.pi, h=4):
    points_under_curve = 0
    for _ in range(num_samples):
        x = a + random.random() * (b - a)
        y = random.random() * h
        if y < f(x):
            points_under_curve += 1
    area = (b - a) * h
    return (area * points_under_curve) / num_samples


class RoundedButton(tk.Canvas):
    def __init__(self, parent, text, command, width=120, height=40,
                 corner_radius=10, bg='#2D2D2D', fg='white', hover_bg='#3D3D3D',
                 font=('Segoe UI', 10)):
        super().__init__(parent, width=width, height=height,
                         bg=parent["bg"], highlightthickness=0)

        self.command = command
        self.bg = bg
        self.fg = fg
        self.hover_bg = hover_bg
        self.corner_radius = corner_radius

        self.create_rounded_rect = self.create_rounded_rectangle(
            0, 0, width, height, corner_radius, fill=bg, outline=""
        )

        self.button_text = self.create_text(
            width / 2, height / 2, text=text, fill=fg, font=font
        )

        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)
        self.bind("<Button-1>", self.on_click)
        self.bind("<ButtonRelease-1>", self.on_release)

    def create_rounded_rectangle(self, x1, y1, x2, y2, radius, **kwargs):
        points = [
            x1 + radius, y1,
            x2 - radius, y1,
            x2, y1,
            x2, y1 + radius,
            x2, y2 - radius,
            x2, y2,
            x2 - radius, y2,
            x1 + radius, y2,
            x1, y2,
            x1, y2 - radius,
            x1, y1 + radius,
            x1, y1
        ]
        return self.create_polygon(points, **kwargs, smooth=True)

    def on_enter(self, event):
        self.itemconfig(self.create_rounded_rect, fill=self.hover_bg)

    def on_leave(self, event):
        self.itemconfig(self.create_rounded_rect, fill=self.bg)

    def on_click(self, event):
        self.itemconfig(self.create_rounded_rect, fill=self.bg)

    def on_release(self, event):
        self.itemconfig(self.create_rounded_rect, fill=self.hover_bg)
        if self.command:
            self.command()


class MonteCarloSurfaceCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Surface Area Calculator - Monte Carlo Method")
        self.root.geometry("800x600")

        self.entry_bg, self.text_color = configure_style(self.root)

        self.main_frame = ttk.Frame(self.root)
        self.main_frame.pack(padx=20, pady=20, fill=tk.BOTH, expand=True)

        title_label = tk.Label(
            self.main_frame,
            text="Monte Carlo Surface Area Calculator",
            font=('Segoe UI', 14, 'bold'),
            bg='#121212',
            fg='#FFFFFF'
        )
        title_label.pack(pady=(0, 15), anchor=tk.CENTER)

        self.param_frame = ttk.LabelFrame(self.main_frame, text="")
        self.param_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))

        for child in self.param_frame.winfo_children():
            if isinstance(child, ttk.Label):
                child.configure(anchor=tk.CENTER)

        param_container = tk.Frame(self.param_frame, bg='#121212')
        param_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.param_entries = {}
        param_labels = ["Samples", "Start (a)", "End (b)", "Height (h)"]
        default_values = ["1000000", "0", str(2 * math.pi), "4"]


        for i, (label, default) in enumerate(zip(param_labels, default_values)):
            frame = tk.Frame(param_container, bg='#121212')
            frame.pack(fill=tk.X, pady=10)

            param_frame = tk.Frame(frame, bg='#121212')
            param_frame.pack(anchor=tk.CENTER, expand=True)

            param_label = tk.Label(
                param_frame,
                text=f"{label}:",
                font=('Segoe UI', 10),
                bg='#121212',
                fg='#FFFFFF',
                width=12,
                anchor='e'
            )
            param_label.pack(side=tk.LEFT, padx=(0, 5))

            entry = tk.Entry(
                param_frame,
                bg=self.entry_bg,
                fg=self.text_color,
                insertbackground=self.text_color,
                relief='flat',
                highlightthickness=1,
                highlightbackground='#333333',
                highlightcolor='#4D4D4D',
                font=('Segoe UI', 10),
                width=15,
                justify=tk.CENTER
            )
            entry.insert(0, default)
            entry.pack(side=tk.LEFT, fill=tk.X, expand=True)

            self.param_entries[label] = entry

        self.button_frame = tk.Frame(self.main_frame, bg='#121212')
        self.button_frame.pack(fill=tk.X, pady=10)

        button_container = tk.Frame(self.button_frame, bg='#121212')
        button_container.pack(anchor=tk.CENTER)

        self.calc_button = RoundedButton(
            button_container,
            text="Calculate Surface Area",
            command=self.run_monte_carlo,
            width=180,
            height=36,
            corner_radius=18,
            bg='#2D2D2D',
            hover_bg='#3D3D3D'
        )
        self.calc_button.pack(side=tk.LEFT, padx=10)

        self.reset_button = RoundedButton(
            button_container,
            text="Reset",
            command=self.reset_parameters,
            width=120,
            height=36,
            corner_radius=18,
            bg='#2D2D2D',
            hover_bg='#3D3D3D'
        )
        self.reset_button.pack(side=tk.LEFT)

        result_frame = tk.Frame(self.main_frame, bg='#121212')
        result_frame.pack(fill=tk.X, pady=15)

        self.result_label = tk.Label(
            result_frame,
            text="Result: ",
            font=('Segoe UI', 11, 'bold'),
            bg='#121212',
            fg='#FFFFFF',
            anchor='center',
            pady=10
        )
        self.result_label.pack(fill=tk.X)

    def run_monte_carlo(self):
        try:
            num_samples = int(self.param_entries["Samples"].get())
            a = float(self.param_entries["Start (a)"].get())
            b = float(self.param_entries["End (b)"].get())
            h = float(self.param_entries["Height (h)"].get())

            surface_area = calculate_surface_monte_carlo(num_samples, a, b, h)
            self.result_label.config(text=f"Surface Area: {surface_area:.6f}")
        except ValueError:
            self.result_label.config(text="Invalid input. Please enter numeric values.")

    def reset_parameters(self):
        defaults = {
            "Samples": "1000000",
            "Start (a)": "0",
            "End (b)": str(2 * math.pi),
            "Height (h)": "4"
        }

        for label, entry in self.param_entries.items():
            entry.delete(0, tk.END)
            entry.insert(0, defaults[label])

        self.result_label.config(text="Result: ")


if __name__ == "__main__":
    root = tk.Tk()
    app = MonteCarloSurfaceCalculator(root)
    root.mainloop()