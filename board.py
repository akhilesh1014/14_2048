import random

SIZE = 4


class Board:
    def __init__(self):
        self.grid = [[0] * SIZE for _ in range(SIZE)]
        self.score = 0
        self.add_random_tile()
        self.add_random_tile()

    def add_random_tile(self):
        empty = [
            (r, c)
            for r in range(SIZE)
            for c in range(SIZE)
            if self.grid[r][c] == 0
        ]

        if empty:
            r, c = random.choice(empty)
            self.grid[r][c] = 4 if random.random() < 0.1 else 2

    @staticmethod
    def slide_line(line):
        values = [x for x in line if x]
        result = []

        i = 0
        while i < len(values):
            if i + 1 < len(values) and values[i] == values[i + 1]:
                result.append(values[i] * 2)
                i += 2
            else:
                result.append(values[i])
                i += 1

        return result + [0] * (SIZE - len(result))

    @staticmethod
    def slide_line_with_score(line):
        values = [x for x in line if x]
        result = []
        score_gained = 0

        i = 0
        while i < len(values):
            if i + 1 < len(values) and values[i] == values[i + 1]:
                merged = values[i] * 2
                result.append(merged)
                score_gained += merged
                i += 2
            else:
                result.append(values[i])
                i += 1

        return result + [0] * (SIZE - len(result)), score_gained

    def move_left(self):
        changed = False

        for r in range(SIZE):
            old = self.grid[r][:]
            new, gained = self.slide_line_with_score(old)

            self.grid[r] = new
            self.score += gained

            if old != new:
                changed = True

        return changed

    def move_right(self):
        changed = False

        for r in range(SIZE):
            old = self.grid[r][:]
            reversed_old = list(reversed(old))

            new_reversed, gained = self.slide_line_with_score(reversed_old)
            new = list(reversed(new_reversed))

            self.grid[r] = new
            self.score += gained

            if old != new:
                changed = True

        return changed

    def move_up(self):
        changed = False

        for c in range(SIZE):
            old = [self.grid[r][c] for r in range(SIZE)]

            new, gained = self.slide_line_with_score(old)

            for r in range(SIZE):
                self.grid[r][c] = new[r]

            self.score += gained

            if old != new:
                changed = True

        return changed

    def move_down(self):
        changed = False

        for c in range(SIZE):
            old = [self.grid[r][c] for r in range(SIZE)]
            reversed_old = list(reversed(old))

            new_reversed, gained = self.slide_line_with_score(reversed_old)
            new = list(reversed(new_reversed))

            for r in range(SIZE):
                self.grid[r][c] = new[r]

            self.score += gained

            if old != new:
                changed = True

        return changed

    def can_move(self):
        if any(0 in row for row in self.grid):
            return True

        for r in range(SIZE):
            for c in range(SIZE):
                if c + 1 < SIZE and self.grid[r][c] == self.grid[r][c + 1]:
                    return True

                if r + 1 < SIZE and self.grid[r][c] == self.grid[r + 1][c]:
                    return True

        return False