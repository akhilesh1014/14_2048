from board import Board


class Game:
    def __init__(self):
        self.board = Board()
        self.score = 0

        self.previous_grid = None
        self.previous_score = 0
        self.best_score = self.score

    def display(self):
        print("\n" + "+------+------+------+------+")
        for row in self.board.grid:
            print("|" + "|".join(f"{x:^6}" if x else f"{' ':^6}" for x in row) + "|")
            print("+------+------+------+------+")
        print("Score:", self.board.score, " Best:", self.best_score)

    def has_won(self):
        return any(2048 in row for row in self.board.grid)

    def is_game_over(self):
        return not self.board.can_move()

    def move(self, key):
        moves = {
            "a": self.board.move_left,
            "d": self.board.move_right,
            "w": self.board.move_up,
            "s": self.board.move_down
        }

        if key not in moves:
            return False

        # Save current state before attempting the move
        old_grid = [row[:] for row in self.board.grid]
        old_score = self.score

        changed = moves[key]()

        # Only a successful move creates/updates undo state
        if changed:
            self.previous_grid = old_grid
            self.previous_score = old_score

            self.board.add_random_tile()

            self.best_score = max(self.best_score, self.score)

        return changed

    def undo(self):
        if self.previous_grid is None:
            return False

        self.board.grid = [row[:] for row in self.previous_grid]
        self.score = self.previous_score

        # One-level undo: consume the saved state
        self.previous_grid = None

        return True

    def run(self):
        print("2048 — W/A/S/D to move, U to undo, Q to quit.")
        while True:
            self.display()

            if self.has_won():
                print("You reached 2048!")
                return

            if self.is_game_over():
                print("No legal moves remain.")
                return
            key = input("> ").strip().lower()
            if key == "q":
                return
            if key == "u":
                self.undo()
            
            if key not in "wasd":
                print("Use W/A/S/D.")
                continue
            if self.move(key):
                self.best_score = max(self.best_score, self.board.score)
