import random
import pygame

# Grid settings
ROWS = 46
COLS = 46
CELL_SIZE = 11
WINDOW_SIZE = COLS * CELL_SIZE
FPS = 15  # default simulation speed, used by UI

# Colors
WHITE = (240, 240, 240)
BLACK = (20, 20, 20)
GRID_COLOR = (170, 170, 170)
BG_COLOR = (230, 230, 230)

# The grid is a list of rows, each row is a list of 0s and 1s
# 0 = dead cell, 1 = alive cell
grid = []
for row in range(ROWS):
    grid.append([0] * COLS)


def make_empty_grid(num_rows, num_cols):
    new_grid = []
    for row in range(num_rows):
        new_grid.append([0] * num_cols)
    return new_grid


def reset_module_grid():
    global grid
    grid = make_empty_grid(ROWS, COLS)
    return grid


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
    # We work on a copy so all cells update at the same time
    new_grid = make_empty_grid(num_rows, num_cols)
    for row in range(num_rows):
        for col in range(num_cols):
            new_grid[row][col] = grid[row][col]

    for row in range(num_rows):
        for col in range(num_cols):
            live_neighbours = count_neighbours(grid, row, col, num_rows, num_cols)

            if grid[row][col] == 1:
                # A live cell dies if it has fewer than 2 or more than 3 neighbours
                if live_neighbours < 2 or live_neighbours > 3:
                    new_grid[row][col] = 0
            else:
                # A dead cell becomes alive if it has exactly 3 neighbours
                if live_neighbours == 3:
                    new_grid[row][col] = 1

    return new_grid


def randomize_grid(grid, num_rows, num_cols):
    for row in range(num_rows):
        for col in range(num_cols):
            if random.random() < 0.3:
                grid[row][col] = 1
            else:
                grid[row][col] = 0


def clear_grid(grid, num_rows, num_cols):
    for row in range(num_rows):
        for col in range(num_cols):
            grid[row][col] = 0


def toggle_cell(grid, row, col, num_rows, num_cols):
    if 0 <= row < num_rows and 0 <= col < num_cols:
        if grid[row][col] == 1:
            grid[row][col] = 0
        else:
            grid[row][col] = 1


def place_pattern_center(grid, pattern_coords, num_rows, num_cols):
    clear_grid(grid, num_rows, num_cols)

    # Find the size of the pattern
    max_row = 0
    max_col = 0
    for row, col in pattern_coords:
        if row > max_row:
            max_row = row
        if col > max_col:
            max_col = col

    # Calculate where to start so the pattern is centered
    start_row = (num_rows - max_row - 1) // 2
    start_col = (num_cols - max_col - 1) // 2

    for row, col in pattern_coords:
        target_row = start_row + row
        target_col = start_col + col
        if 0 <= target_row < num_rows and 0 <= target_col < num_cols:
            grid[target_row][target_col] = 1


def count_live_cells(grid, num_rows, num_cols):
    live_cells = 0
    for row in range(num_rows):
        for col in range(num_cols):
            if grid[row][col] == 1:
                live_cells = live_cells + 1
    return live_cells


def draw_grid(screen, game_grid, num_rows, num_cols, cell_size, offset_x=0, offset_y=0):
    background_rect = pygame.Rect(offset_x, offset_y, num_cols * cell_size, num_rows * cell_size)
    pygame.draw.rect(screen, BG_COLOR, background_rect)

    for row in range(num_rows):
        for col in range(num_cols):
            if game_grid[row][col] == 1:
                color = BLACK
            else:
                color = WHITE
            x = offset_x + col * cell_size
            y = offset_y + row * cell_size
            rect = pygame.Rect(x, y, cell_size, cell_size)
            pygame.draw.rect(screen, color, rect)
            pygame.draw.rect(screen, GRID_COLOR, rect, 1)