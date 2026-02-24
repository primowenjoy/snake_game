import random
import tkinter as tk


class SnakeGame:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("Snake")
        self.root.resizable(False, False)

        self.cell_size = 20
        self.grid_width = 30
        self.grid_height = 20
        self.board_width = self.grid_width * self.cell_size
        self.board_height = self.grid_height * self.cell_size
        self.tick_ms = 120

        self.score_var = tk.StringVar(value="Score: 0")
        self.status_var = tk.StringVar(value="Use arrow keys to move")

        top_bar = tk.Frame(self.root)
        top_bar.pack(fill="x", padx=8, pady=(8, 0))
        tk.Label(top_bar, textvariable=self.score_var, font=("Helvetica", 12, "bold")).pack(
            side="left"
        )
        tk.Label(top_bar, textvariable=self.status_var, font=("Helvetica", 11)).pack(
            side="right"
        )

        self.canvas = tk.Canvas(
            self.root,
            width=self.board_width,
            height=self.board_height,
            bg="#1d1f21",
            highlightthickness=0,
        )
        self.canvas.pack(padx=8, pady=8)

        self.root.bind("<Up>", lambda _: self.change_direction((0, -1)))
        self.root.bind("<Down>", lambda _: self.change_direction((0, 1)))
        self.root.bind("<Left>", lambda _: self.change_direction((-1, 0)))
        self.root.bind("<Right>", lambda _: self.change_direction((1, 0)))
        self.root.bind("<r>", lambda _: self.restart())
        self.root.bind("<R>", lambda _: self.restart())

        self.after_id: str | None = None
        self.restart()

    def restart(self) -> None:
        if self.after_id:
            self.root.after_cancel(self.after_id)
            self.after_id = None

        center_x = self.grid_width // 2
        center_y = self.grid_height // 2
        self.snake = [(center_x, center_y), (center_x - 1, center_y), (center_x - 2, center_y)]
        self.direction = (1, 0)
        self.pending_direction = self.direction
        self.score = 0
        self.game_over = False
        self.status_var.set("Use arrow keys to move")
        self.score_var.set(f"Score: {self.score}")

        self.food = self.random_empty_cell()
        self.draw()
        self.tick()

    def random_empty_cell(self) -> tuple[int, int]:
        occupied = set(self.snake)
        free_cells = [
            (x, y)
            for x in range(self.grid_width)
            for y in range(self.grid_height)
            if (x, y) not in occupied
        ]
        return random.choice(free_cells)

    def change_direction(self, new_direction: tuple[int, int]) -> None:
        if self.game_over:
            return

        dx, dy = self.direction
        ndx, ndy = new_direction
        if (dx + ndx, dy + ndy) == (0, 0):
            return
        self.pending_direction = new_direction

    def tick(self) -> None:
        if self.game_over:
            return

        self.direction = self.pending_direction
        head_x, head_y = self.snake[0]
        dx, dy = self.direction
        new_head = (head_x + dx, head_y + dy)

        if self.is_collision(new_head):
            self.end_game()
            return

        self.snake.insert(0, new_head)
        if new_head == self.food:
            self.score += 1
            self.score_var.set(f"Score: {self.score}")
            self.food = self.random_empty_cell()
        else:
            self.snake.pop()

        self.draw()
        self.after_id = self.root.after(self.tick_ms, self.tick)

    def is_collision(self, pos: tuple[int, int]) -> bool:
        x, y = pos
        if x < 0 or x >= self.grid_width or y < 0 or y >= self.grid_height:
            return True
        if pos in self.snake:
            return True
        return False

    def end_game(self) -> None:
        self.game_over = True
        self.status_var.set("Game over - press R to restart")
        self.draw()

    def draw(self) -> None:
        self.canvas.delete("all")
        self.draw_checkerboard()

        food_x, food_y = self.food
        self.draw_cell(food_x, food_y, "#e74c3c")

        for i, (x, y) in enumerate(self.snake):
            color = "#2ecc71" if i == 0 else "#27ae60"
            self.draw_cell(x, y, color)

    def draw_checkerboard(self) -> None:
        for x in range(self.grid_width):
            for y in range(self.grid_height):
                base = "#2b2f33" if (x + y) % 2 == 0 else "#25292d"
                x1 = x * self.cell_size
                y1 = y * self.cell_size
                x2 = x1 + self.cell_size
                y2 = y1 + self.cell_size
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=base, outline=base)

    def draw_cell(self, x: int, y: int, color: str) -> None:
        pad = 2
        x1 = x * self.cell_size + pad
        y1 = y * self.cell_size + pad
        x2 = (x + 1) * self.cell_size - pad
        y2 = (y + 1) * self.cell_size - pad
        self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline=color)


def main() -> None:
    root = tk.Tk()
    SnakeGame(root)
    root.mainloop()


if __name__ == "__main__":
    main()
