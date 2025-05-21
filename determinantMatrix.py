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

    style.configure('TLabel',
                    background=bg_color,
                    foreground=text_color,
                    font=default_font)

    style.configure('TLabelframe',
                    background=bg_color,
                    foreground=text_color,
                    relief='flat',
                    borderwidth=1)

    style.configure('TLabelframe.Label',
                    font=title_font,
                    background=bg_color,
                    foreground=text_color)

    style.configure('Result.TLabel',
                    background=bg_color,
                    foreground=text_color,
                    font=title_font,
                    relief='flat',
                    borderwidth=0)

    style.configure('RoundButton.TButton',
                    background=button_bg,
                    foreground=text_color,
                    borderwidth=0,
                    relief='flat',
                    font=default_font,
                    padding=8)

    style.map('RoundButton.TButton',
              background=[('active', button_active), ('pressed', button_bg)],
              foreground=[('active', text_color), ('pressed', text_color)])


def calculate_determinant(matrix):
    n = len(matrix)
    if n == 1:
        return matrix[0][0]
    if n == 2:
        return matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]

    det = 0
    for i in range(n):
        submatrix = create_submatrix(matrix, 0, i)
        cofactor = (-1) ** i * matrix[0][i]
        det += cofactor * calculate_determinant(submatrix)
    return det


def create_submatrix(matrix, row_to_remove, col_to_remove):
    return [
        [elem for j, elem in enumerate(row) if j != col_to_remove]
        for i, row in enumerate(matrix) if i != row_to_remove
    ]


def get_matrix_input(matrix_str):
    rows = matrix_str.strip().split('\n')
    return [list(map(float, row.split(','))) for row in rows]


def run_determinant():
    try:
        matrix_string = matrix_entry.get("1.0", tk.END)
        matrix = get_matrix_input(matrix_string)
        determinant = calculate_determinant(matrix)
        result_label.config(text=f"Determinant: {determinant}")
    except ValueError:
        result_label.config(text="Invalid data. Enter only numbers.")
    except Exception as e:
        result_label.config(text=f"ERROR: {e}")


window = tk.Tk()
window.title("Determinant of the Matrix")
window.geometry("800x500")

configure_style(window)


main_frame = ttk.Frame(window)
main_frame.pack(padx=20, pady=20, fill=tk.BOTH, expand=True)


matrix_frame = ttk.LabelFrame(
    main_frame,
    text="Enter matrix (comma separated values, new lines on new lines)"
)
matrix_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))

matrix_entry = tk.Text(
    matrix_frame,
    height=6,
    bg='#252526',
    fg='#FFFFFF',
    insertbackground='#FFFFFF',
    padx=10,
    pady=10,
    wrap=tk.WORD,
    font=('Consolas', 10),
    relief='flat',
    highlightthickness=0,
    borderwidth=0
)
matrix_entry.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

button_frame = tk.Frame(main_frame, bg='#121212')
button_frame.pack(fill=tk.X, pady=5)


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

calc_button = RoundedButton(
    button_frame,
    text="Calculate Determinant",
    command=run_determinant,
    width=180,
    height=36,
    corner_radius=18,
    bg='#2D2D2D',
    hover_bg='#3D3D3D'
)
calc_button.pack(pady=5)

result_label = tk.Label(
    main_frame,
    text=" Result: ",
    font=('Segoe UI', 11, 'bold'),
    anchor='center',
    bg='#121212',
    fg='#FFFFFF',
    bd=0,
    highlightthickness=0
)
result_label.pack(fill=tk.X, pady=10)

window.mainloop()
