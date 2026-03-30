import random

WINDOW_SIZE = 506
ROWS = 46
COLS = 46
CELL_SIZE = WINDOW_SIZE // ROWS
FPS = 15

WHITE = (240, 240, 240)
BLACK = (20, 20, 20)
GRID_COLOR = (170, 170, 170)
BG_COLOR = (230, 230, 230)

grid = []
for row in range(ROWS):
    new_row = []
    for col in range(COLS):
        new_row.append(0)
    grid.append(new_row)


def count_neighbours(grid, row, col, num_rows, num_cols):
    neighbours = 0

    for dr in [-1, 0, 1]:
        for dc in [-1, 0, 1]:
            if dr == 0 and dc == 0:
                continue

            r = row + dr
            c = col + dc

            if 0 <= r < num_rows and 0 <= c < num_cols:
                if grid[r][c] == 1:
                    neighbours = neighbours + 1

    return neighbours


def next_generation(grid, num_rows, num_cols):
    new_grid = []
    for row in range(num_rows):
        copied_row = []
        for col in range(num_cols):
            copied_row.append(grid[row][col])
        new_grid.append(copied_row)

    for row in range(num_rows):
        for col in range(num_cols):
            live_neighbours = count_neighbours(grid, row, col, num_rows, num_cols)

            if grid[row][col] == 1:
                if live_neighbours < 2:
                    new_grid[row][col] = 0
                elif live_neighbours == 2 or live_neighbours == 3:
                    new_grid[row][col] = 1
                else:
                    new_grid[row][col] = 0
            else:
                if live_neighbours == 3:
                    new_grid[row][col] = 1
                else:
                    new_grid[row][col] = 0

    return new_grid


def randomize_grid(grid, num_rows, num_cols):
    for row in range(num_rows):
        for col in range(num_cols):
            if random.random() < 0.3:
                grid[row][col] = 1
            else:
                grid[row][col] = 0


def count_live_cells(grid, num_rows, num_cols):
    live_cells = 0

    for row in range(num_rows):
        for col in range(num_cols):
            if grid[row][col] == 1:
                live_cells = live_cells + 1

    return live_cells
