import tkinter as tk
from tkinter import ttk


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


def get_polynomial_value(x, a=1, b=1, c=1, d=1, e=1, f=1):
    return a * x ** 5 + b * x ** 4 + c * x ** 3 + d * x ** 2 + e * x + f


def same_sign(n1, n2):
    return (n1 * n2) > 0


def find_roots_bisection(a=1, b=1, c=1, d=1, e=1, f=1, min_val=-100, max_val=100,
                         epsilon=0.00001, move=0.001):
    roots = []
    left = min_val
    while left < max_val:
        if same_sign(get_polynomial_value(left, a, b, c, d, e, f), get_polynomial_value(left +
                                                                                        move, a, b, c, d, e, f)):
            left += move
        else:
            left_bisection = left
            right_bisection = left + move
            while (right_bisection - left_bisection) > epsilon:
                mid = (left_bisection + right_bisection) / 2
                if same_sign(get_polynomial_value(left_bisection, a, b, c, d, e, f),
                             get_polynomial_value(mid, a, b, c, d, e, f)):
                    left_bisection = mid
                else:
                    right_bisection = mid
            roots.append(round(mid, len(str(epsilon)) - 2))
            left = right_bisection
    return roots


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


class BisectionRootFinder:
    def __init__(self, root):
        self.root = root
        self.root.title("Polynomial Root Finder - Bisection Method")
        self.root.geometry("800x600")

        self.entry_bg, self.text_color = configure_style(self.root)

        self.main_frame = ttk.Frame(self.root)
        self.main_frame.pack(padx=20, pady=20, fill=tk.BOTH, expand=True)

        # Center the title text
        title_label = tk.Label(
            self.main_frame,
            text="Polynomial Root Finder",
            font=('Segoe UI', 14, 'bold'),
            bg='#121212',
            fg='#FFFFFF'
        )
        title_label.pack(pady=(0, 15), anchor=tk.CENTER)

        self.poly_frame = ttk.LabelFrame(self.main_frame, text="Polynomial Coefficients")
        self.poly_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))

        # Center the LabelFrame title
        for child in self.poly_frame.winfo_children():
            if isinstance(child, ttk.Label):
                child.configure(anchor=tk.CENTER)

        self.coef_entries = {}
        coef_labels = ["a", "b", "c", "d", "e", "f"]
        default_values = ["1", "1", "1", "1", "1", "1"]

        coef_container = tk.Frame(self.poly_frame, bg='#121212')
        coef_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        for i, (label, default) in enumerate(zip(coef_labels, default_values)):
            row, col = divmod(i, 3)

            frame = tk.Frame(coef_container, bg='#121212')
            frame.grid(row=row, column=col, padx=20, pady=10, sticky="nsew")

            coef_frame = tk.Frame(frame, bg='#121212')
            coef_frame.pack(anchor=tk.CENTER, expand=True)

            coef_label = tk.Label(
                coef_frame,
                text=f"{label}:",
                font=('Segoe UI', 10),
                bg='#121212',
                fg='#FFFFFF',
                width=3,
                anchor='e'
            )
            coef_label.pack(side=tk.LEFT, padx=(0, 5))

            entry = tk.Entry(
                coef_frame,
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

            self.coef_entries[label] = entry

        # Make columns expand equally
        coef_container.grid_columnconfigure((0, 1, 2), weight=1, uniform="coef")

        self.param_frame = ttk.LabelFrame(self.main_frame, text="Search Parameters")
        self.param_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))

        # Center the LabelFrame title
        for child in self.param_frame.winfo_children():
            if isinstance(child, ttk.Label):
                child.configure(anchor=tk.CENTER)

        self.param_entries = {}
        param_labels = ["min", "max", "epsilon", "move"]
        default_values = ["-100", "100", "0.00001", "0.001"]

        param_container = tk.Frame(self.param_frame, bg='#121212')
        param_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        for i, (label, default) in enumerate(zip(param_labels, default_values)):
            row, col = divmod(i, 2)

            frame = tk.Frame(param_container, bg='#121212')
            frame.grid(row=row, column=col, padx=20, pady=10, sticky="nsew")

            # Center the parameter entry
            param_frame = tk.Frame(frame, bg='#121212')
            param_frame.pack(anchor=tk.CENTER, expand=True)

            param_label = tk.Label(
                param_frame,
                text=f"{label}:",
                font=('Segoe UI', 10),
                bg='#121212',
                fg='#FFFFFF',
                width=8,
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

        # Make columns expand equally
        param_container.grid_columnconfigure((0, 1), weight=1, uniform="param")

        # Center the buttons
        self.button_frame = tk.Frame(self.main_frame, bg='#121212')
        self.button_frame.pack(fill=tk.X, pady=10)

        # Center the buttons in the frame
        button_container = tk.Frame(self.button_frame, bg='#121212')
        button_container.pack(anchor=tk.CENTER)

        self.calc_button = RoundedButton(
            button_container,
            text="Calculate Roots",
            command=self.run_bisection,
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

        # Center the result text
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

    def run_bisection(self):
        try:
            a = float(self.coef_entries["a"].get())
            b = float(self.coef_entries["b"].get())
            c = float(self.coef_entries["c"].get())
            d = float(self.coef_entries["d"].get())
            e = float(self.coef_entries["e"].get())
            f = float(self.coef_entries["f"].get())

            min_val = float(self.param_entries["min"].get())
            max_val = float(self.param_entries["max"].get())
            epsilon = float(self.param_entries["epsilon"].get())
            move = float(self.param_entries["move"].get())

            roots = find_roots_bisection(a, b, c, d, e, f, min_val, max_val, epsilon, move)

            self.result_label.config(text=f"Found roots: {roots}")

        except ValueError:
            self.result_label.config(text="Invalid input. Please enter numeric values.")

    def reset_parameters(self):
        for label, entry in self.coef_entries.items():
            entry.delete(0, tk.END)
            entry.insert(0, "1")

        defaults = {
            "min": "-100",
            "max": "100",
            "epsilon": "0.00001",
            "move": "0.001"
        }

        for label, entry in self.param_entries.items():
            entry.delete(0, tk.END)
            entry.insert(0, defaults[label])

        self.result_label.config(text="Result: ")


if __name__ == "__main__":
    root = tk.Tk()
    app = BisectionRootFinder(root)
    root.mainloop()