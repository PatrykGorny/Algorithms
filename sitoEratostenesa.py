import tkinter as tk
from tkinter import ttk


def configure_style():
    style = ttk.Style()
    style.theme_use('clam')

    bg_color = '#121212'
    frame_bg = '#1E1E1E'
    button_bg = '#2D2D2D'
    button_active = '#3D3D3D'
    text_color = '#FFFFFF'
    entry_bg = '#252526'
    border_color = '#333333'

    default_font = ('Segoe UI', 10)
    title_font = ('Segoe UI', 14, 'bold')

    window.configure(bg=bg_color)

    style.configure('TFrame', background=bg_color)

    style.configure('Header.TLabel',
                    font=title_font,
                    background=bg_color,
                    foreground=text_color)

    style.configure('TLabel',
                    font=default_font,
                    background=bg_color,
                    foreground=text_color)

    style.configure('TEntry',
                    font=default_font,
                    fieldbackground=entry_bg,
                    foreground=text_color,
                    borderwidth=0,
                    relief='flat')


def sieve_of_eratosthenes(limit):
    is_prime = [True] * (limit + 1)
    is_prime[0:2] = [False, False]
    for number in range(2, int(limit ** 0.5) + 1):
        if is_prime[number]:
            for multiple in range(number * number, limit + 1, number):
                is_prime[multiple] = False
    return [index for index, prime in enumerate(is_prime) if prime]


def on_find_primes():
    try:
        limit = int(limit_entry.get())
        primes = sieve_of_eratosthenes(limit)
        result_text.delete("1.0", tk.END)
        result_text.insert(tk.END, f"Prime numbers to {limit}:\n" + ", ".join(map(str, primes)))
    except ValueError:
        result_text.delete("1.0", tk.END)
        result_text.insert(tk.END, "Invalid data. Please enter an integer.")


window = tk.Tk()
window.title("Sieve of Eratosthenes")
window.geometry("600x500")
configure_style()

main_frame = ttk.Frame(window)
main_frame.pack(padx=20, pady=20, fill=tk.BOTH, expand=True)

header_label = ttk.Label(main_frame, text="Sieve of Eratosthenes", style='Header.TLabel')
header_label.pack(pady=(0, 15))

input_frame = ttk.Frame(main_frame)
input_frame.pack(fill=tk.X, pady=5)

ttk.Label(input_frame, text="Upper limit:").pack(pady=(5, 2), anchor='w')
limit_entry = ttk.Entry(input_frame)
limit_entry.pack(pady=5, fill='x')

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


button_frame = tk.Frame(main_frame, bg='#121212')
button_frame.pack(fill=tk.X, pady=10)

find_primes_button = RoundedButton(
    button_frame,
    text="Find Prime Numbers",
    command=on_find_primes,
    width=250,
    height=36,
    corner_radius=18,
    bg='#2D2D2D',
    hover_bg='#3D3D3D'
)
find_primes_button.pack(pady=5)

result_frame = ttk.Frame(main_frame)
result_frame.pack(fill=tk.BOTH, expand=True, pady=10)

result_text = tk.Text(
    result_frame,
    wrap='word',
    bg='#252526',
    fg='#FFFFFF',
    insertbackground='white',
    font=('Consolas', 10),
    relief='flat',
    borderwidth=0,
    highlightthickness=0
)
result_text.pack(fill='both', expand=True)


window.update()
for widget in window.winfo_children():
    if isinstance(widget, ttk.Frame):
        widget.configure(style='TFrame')

window.mainloop()