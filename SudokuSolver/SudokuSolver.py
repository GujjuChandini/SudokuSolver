import tkinter as tk
from tkinter import ttk

class SudokuSolver:
    def __init__(self, root):
        self.root = root
        self.root.title("Sudoku Solver")
        self.board = [[0 for _ in range(9)] for _ in range(9)]
        self.entries = [[None for _ in range(9)] for _ in range(9)]
        self.create_widgets()
        self.is_paused = False
        self.timer = None
        self.speed = 500

    def create_widgets(self):
        heading = ttk.Label(self.root, text="Sudoku Solver", font=("Arial", 24))
        heading.pack(pady=10)
        
        frame = ttk.Frame(self.root)
        frame.pack(padx=10, pady=10)

        for i in range(9):
            for j in range(9):
                self.entries[i][j] = ttk.Entry(frame, width=2, font=("Arial", 24), justify='center')
                self.entries[i][j].grid(row=i, column=j, padx=5, pady=5)

        self.solve_button = ttk.Button(self.root, text="Solve", command=self.start_solving)
        self.solve_button.pack(pady=10)

        self.pause_button = ttk.Button(self.root, text="Pause", command=self.toggle_pause)
        self.pause_button.pack(pady=10)

        self.speed_label = ttk.Label(self.root, text="Speed:")
        self.speed_label.pack(pady=10)

        self.speed_slider = ttk.Scale(self.root, from_=1000, to=100, orient='horizontal', command=self.update_speed)
        self.speed_slider.set(500)
        self.speed_slider.pack(pady=10)

    def update_speed(self, value):
        self.speed = int(float(value))
        if self.timer:
            self.root.after_cancel(self.timer)
            self.timer = self.root.after(self.speed, self.solve_step)

    def toggle_pause(self):
        self.is_paused = not self.is_paused
        self.pause_button.config(text="Resume" if self.is_paused else "Pause")
        if not self.is_paused:
            self.timer = self.root.after(self.speed, self.solve_step)

    def start_solving(self):
        for i in range(9):
            for j in range(9):
                value = self.entries[i][j].get()
                self.board[i][j] = int(value) if value.isdigit() else 0

        self.solve_button.config(state="disabled")
        self.solve_step()

    def solve_step(self):
        if self.is_paused:
            return

        if self.solve_sudoku():
            self.solve_button.config(state="normal")
            self.show_message("Sudoku Solved!")
        else:
            self.show_message("No Solution Exists!")
        
    def show_message(self, message):
        message_label = ttk.Label(self.root, text=message, font=("Arial", 16))
        message_label.pack(pady=10)

    def solve_sudoku(self):
        empty = self.find_empty()
        if not empty:
            return True

        row, col = empty
        for num in range(1, 10):
            if self.is_valid(num, row, col):
                self.board[row][col] = num
                self.entries[row][col].delete(0, tk.END)
                self.entries[row][col].insert(0, str(num))
                self.root.update()
                self.root.after(self.speed)

                if self.solve_sudoku():
                    return True

                self.board[row][col] = 0
                self.entries[row][col].delete(0, tk.END)
                self.root.update()
                self.root.after(self.speed)

        return False

    def is_valid(self, num, row, col):
        for i in range(9):
            if self.board[row][i] == num or self.board[i][col] == num:
                return False

        box_row = row // 3 * 3
        box_col = col // 3 * 3
        for i in range(box_row, box_row + 3):
            for j in range(box_col, box_col + 3):
                if self.board[i][j] == num:
                    return False

        return True

    def find_empty(self):
        for i in range(9):
            for j in range(9):
                if self.board[i][j] == 0:
                    return (i, j)
        return None

if __name__ == "__main__":
    root = tk.Tk()
    app = SudokuSolver(root)
    root.mainloop()

