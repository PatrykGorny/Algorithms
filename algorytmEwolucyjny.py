import tkinter as tk
from tkinter import ttk
import random
import math


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


class EvolutionaryAlgorithm:
    def __init__(self, population_size=100, generations=100, mutation_rate=0.001, crossover_rate=0.001, elitism_rate=0.001):
        self.population_size = population_size
        self.generations = generations
        self.mutation_rate = mutation_rate
        self.crossover_rate = crossover_rate
        self.elitism_rate = elitism_rate
        self.random = random.Random()
        self.population = []
        for _ in range(self.population_size):
            self.population.append({'x': self.random.uniform(0, 2 * math.pi), 'y': self.random.uniform(0, 2 * math.pi)})

    def fitness(self, x, y):
        return math.sin(x) + math.sin(2 * x) + math.sin(4 * x) + math.sin(8 * x) + math.cos(y) + math.cos(2 * y) + math.cos(4 * y) + math.cos(8 * y)

    def tournament_selection(self):
        tournament_size = 5
        tournament = []
        for _ in range(tournament_size):
            tournament.append(self.population[self.random.randint(0, self.population_size - 1)])
        tournament.sort(key=lambda individual: self.fitness(individual['x'], individual['y']), reverse=True)
        return tournament[0]

    def uniform_crossover(self, parent1, parent2):
        return {
            'x': self.random.choice([parent1['x'], parent2['x']]),
            'y': self.random.choice([parent1['y'], parent2['y']])
        }

    def mutate(self, individual):
        if self.random.random() < self.mutation_rate:
            individual['x'] = self.random.uniform(0, 2 * math.pi)
        if self.random.random() < self.mutation_rate:
            individual['y'] = self.random.uniform(0, 2 * math.pi)
        return individual

    def run(self):
        for _ in range(self.generations):
            self.population.sort(key=lambda individual: self.fitness(individual['x'], individual['y']), reverse=True)
            elitism_count = int(self.elitism_rate * self.population_size)
            new_population = self.population[:elitism_count]
            while len(new_population) < self.population_size:
                parent1 = self.tournament_selection()
                parent2 = self.tournament_selection()
                child = self.uniform_crossover(parent1, parent2)
                child = self.mutate(child)
                new_population.append(child)
            self.population = new_population
        self.population.sort(key=lambda individual: self.fitness(individual['x'], individual['y']), reverse=True)
        return self.population[0]


class EvolutionaryAlgorithmApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Evolutionary Algorithm")
        self.root.geometry("500x600")

        self.entry_bg, self.text_color = configure_style(self.root)

        self.main_frame = ttk.Frame(self.root)
        self.main_frame.pack(padx=20, pady=20, fill=tk.BOTH, expand=True)

        title_label = tk.Label(
            self.main_frame,
            text="Evolutionary Algorithm Optimization",
            font=('Segoe UI', 14, 'bold'),
            bg='#121212',
            fg='#FFFFFF'
        )
        title_label.pack(pady=(0, 15), anchor=tk.CENTER)

        self.param_frame = ttk.LabelFrame(self.main_frame, text="")
        self.param_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))

        param_container = tk.Frame(self.param_frame, bg='#121212')
        param_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.param_entries = {}
        param_labels = ["Population Size", "Generations", "Mutation Rate", "Crossover Rate", "Elitism Rate"]
        default_values = ["100", "100", "0.001", "0.001", "0.001"]

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
                width=15,
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

        self.run_button = RoundedButton(
            button_container,
            text="Run Algorithm",
            command=self.run_evolutionary_algorithm,
            width=180,
            height=36,
            corner_radius=18,
            bg='#2D2D2D',
            hover_bg='#3D3D3D'
        )
        self.run_button.pack(side=tk.LEFT, padx=10)

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

        # Results frame with text output
        results_frame = ttk.LabelFrame(self.main_frame, text="")
        results_frame.pack(fill=tk.BOTH, expand=True, pady=10)

        self.result_text = tk.Text(
            results_frame,
            height=5,
            bg='#1E1E1E',
            fg='#FFFFFF',
            insertbackground='#FFFFFF',
            relief='flat',
            font=('Segoe UI', 10),
            highlightthickness=1,
            highlightbackground='#333333',
            highlightcolor='#4D4D4D',
            padx=10,
            pady=10
        )
        self.result_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    def run_evolutionary_algorithm(self):
        try:
            population_size = int(self.param_entries["Population Size"].get())
            generations = int(self.param_entries["Generations"].get())
            mutation_rate = float(self.param_entries["Mutation Rate"].get())
            crossover_rate = float(self.param_entries["Crossover Rate"].get())
            elitism_rate = float(self.param_entries["Elitism Rate"].get())

            ea = EvolutionaryAlgorithm(population_size, generations, mutation_rate, crossover_rate, elitism_rate)
            best_individual = ea.run()
            fitness_value = ea.fitness(best_individual['x'], best_individual['y'])

            self.result_text.delete("1.0", tk.END)
            self.result_text.insert(
                tk.END,
                f"Best Solution:\nx = {best_individual['x']:.4f}, y = {best_individual['y']:.4f}\n\nFitness Value: {fitness_value:.4f}"
            )
        except ValueError:
            self.result_text.delete("1.0", tk.END)
            self.result_text.insert(tk.END, "Invalid input. Please enter numeric values.")

    def reset_parameters(self):
        defaults = {
            "Population Size": "100",
            "Generations": "100",
            "Mutation Rate": "0.001",
            "Crossover Rate": "0.001",
            "Elitism Rate": "0.001"
        }

        for label, entry in self.param_entries.items():
            entry.delete(0, tk.END)
            entry.insert(0, defaults[label])

        self.result_text.delete("1.0", tk.END)


if __name__ == "__main__":
    root = tk.Tk()
    app = EvolutionaryAlgorithmApp(root)
    root.mainloop()