import random
from collections import deque

ROWS = 10
COLS = 10

start = (0, 0)
goal = (9, 9)

def path_exists(grid):

    queue = deque([start])

    visited = set()

    while queue:

        row, col = queue.popleft()

        if (row, col) == goal:
            return True

        if (row, col) in visited:
            continue

        visited.add((row, col))

        directions = [
            (-1, 0),
            (1, 0),
            (0, -1),
            (0, 1)
        ]

        for dr, dc in directions:

            new_row = row + dr
            new_col = col + dc

            if (
                0 <= new_row < ROWS
                and 0 <= new_col < COLS
                and grid[new_row][new_col] == 0
                and (new_row, new_col) not in visited
            ):

                queue.append((new_row, new_col))

    return False


def generate_maze():

    while True:

        grid = []

        for row in range(ROWS):

            current_row = []

            for col in range(COLS):

                if (row, col) == start or (row, col) == goal:

                    current_row.append(0)

                else:

                    if random.random() < 0.30:
                        current_row.append(1)

                    else:
                        current_row.append(0)

            grid.append(current_row)

        if path_exists(grid):
            return grid


maze = generate_maze()