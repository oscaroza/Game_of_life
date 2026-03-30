import pygame
import grid as gol

ROWS = gol.ROWS
COLS = gol.COLS
WINDOW_SIZE = gol.WINDOW_SIZE
CELL_SIZE = gol.CELL_SIZE
FPS = gol.FPS

WHITE = gol.WHITE
BLACK = gol.BLACK
GRID_COLOR = gol.GRID_COLOR
BG_COLOR = gol.BG_COLOR


def make_empty_grid(num_rows, num_cols):
    new_grid = []
    for row in range(num_rows):
        row_values = []
        for col in range(num_cols):
            row_values.append(0)
        new_grid.append(row_values)
    return new_grid


def draw_grid(screen, game_grid, num_rows, num_cols):
    screen.fill(BG_COLOR)

    for row in range(num_rows):
        for col in range(num_cols):
            if game_grid[row][col] == 1:
                color = BLACK
            else:
                color = WHITE

            rect = pygame.Rect(col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(screen, color, rect)
            pygame.draw.rect(screen, GRID_COLOR, rect, 1)

    pygame.display.flip()


def toggle_cell_from_mouse(game_grid, mouse_pos, num_rows, num_cols):
    x = mouse_pos[0]
    y = mouse_pos[1]

    col = x // CELL_SIZE
    row = y // CELL_SIZE

    if 0 <= row < num_rows and 0 <= col < num_cols:
        if game_grid[row][col] == 1:
            game_grid[row][col] = 0
        else:
            game_grid[row][col] = 1


def run():
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
    clock = pygame.time.Clock()

    game_grid = make_empty_grid(ROWS, COLS)
    gol.randomize_grid(game_grid, ROWS, COLS)

    running = True
    paused = False

    while running:
        clock.tick(FPS)

        live_cells = gol.count_live_cells(game_grid, ROWS, COLS)
        if paused:
            state_text = "PAUSE"
        else:
            state_text = "RUN"
        pygame.display.set_caption(
            "Grid Test - "
            + state_text
            + " - live: "
            + str(live_cells)
            + " - space:pause  r:random  c:clear  click:toggle"
        )

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                toggle_cell_from_mouse(game_grid, event.pos, ROWS, COLS)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    paused = not paused
                elif event.key == pygame.K_r:
                    gol.randomize_grid(game_grid, ROWS, COLS)
                elif event.key == pygame.K_c:
                    game_grid = make_empty_grid(ROWS, COLS)
                    paused = True
                elif event.key == pygame.K_n:
                    game_grid = gol.next_generation(game_grid, ROWS, COLS)
                    paused = True

        if not paused:
            game_grid = gol.next_generation(game_grid, ROWS, COLS)

        draw_grid(screen, game_grid, ROWS, COLS)

    pygame.quit()


if __name__ == "__main__":
    run()
