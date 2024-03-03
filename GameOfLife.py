import tkinter as tk
import numpy as np

class GameOfLife:
    def __init__(self, master, width=50, height=50, cell_size=10):
        self.master = master
        self.master.title("Jeu de la Vie")
        
        self.width = width
        self.height = height
        self.cell_size = cell_size

        self.canvas = tk.Canvas(master, width=self.width * self.cell_size, height=self.height * self.cell_size, borderwidth=0, highlightthickness=0)
        self.canvas.pack()

        self.grid = np.zeros((self.width, self.height), dtype=bool)
        self.running = False
        self.paused = False

        self.draw_grid()

        self.canvas.bind("<Button-1>", self.toggle_cell)
        self.start_button = tk.Button(master, text="Start", command=self.start_game)
        self.start_button.pack(side=tk.LEFT)
        self.stop_button = tk.Button(master, text="Stop", command=self.stop_game)
        self.stop_button.pack(side=tk.LEFT)
        self.pause_button = tk.Button(master, text="Pause", command=self.pause_game)
        self.pause_button.pack(side=tk.LEFT)
        self.clear_button = tk.Button(master, text="Clear", command=self.clear_grid)
        self.clear_button.pack(side=tk.LEFT)

        self.time_label = tk.Label(master, text="Temps écoulé: 0", font=('Arial', 12))
        self.time_label.pack()

        self.time_counter = 0

    def draw_grid(self):
        self.canvas.delete("cell")
        for i in range(self.width):
            for j in range(self.height):
                x0, y0 = i * self.cell_size, j * self.cell_size
                x1, y1 = x0 + self.cell_size, y0 + self.cell_size
                color = "black" if self.grid[i, j] else "white"
                self.canvas.create_rectangle(x0, y0, x1, y1, fill=color, outline="black", tags="cell")

    def toggle_cell(self, event):
        x = event.x // self.cell_size
        y = event.y // self.cell_size
        self.grid[x, y] = not self.grid[x, y]
        self.draw_grid()

    def start_game(self):
        if not self.running:
            self.running = True
            self.run_game()

    def run_game(self):
        if not self.paused:
            self.step()
            self.draw_grid()
            self.time_counter += 1
            self.time_label.config(text=f"Temps écoulé: {self.time_counter}")
            if self.running and not self.is_stable():
                self.master.after(100, self.run_game)

    def stop_game(self):
        self.running = False

    def pause_game(self):
        self.paused = not self.paused

    def clear_grid(self):
        self.grid = np.zeros((self.width, self.height), dtype=bool)
        self.draw_grid()
        self.time_counter = 0
        self.time_label.config(text="Temps écoulé: 0")

    def step(self):
        new_grid = np.zeros((self.width, self.height), dtype=bool)
        for i in range(self.width):
            for j in range(self.height):
                neighbors = self.get_neighbors(i, j)
                if self.grid[i, j]:
                    if neighbors < 2 or neighbors > 3:
                        new_grid[i, j] = False
                    else:
                        new_grid[i, j] = True
                else:
                    if neighbors == 3:
                        new_grid[i, j] = True
        self.grid = new_grid

    def get_neighbors(self, x, y):
        count = 0
        for i in range(max(0, x-1), min(self.width, x+2)):
            for j in range(max(0, y-1), min(self.height, y+2)):
                if (i != x or j != y) and self.grid[i, j]:
                    count += 1
        return count

    def is_stable(self):
        next_grid = np.copy(self.grid)
        self.step()
        result = np.array_equal(self.grid, next_grid)
        self.grid = next_grid
        return result

root = tk.Tk()
game = GameOfLife(root)
root.mainloop()