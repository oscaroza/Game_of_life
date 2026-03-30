import math
import sys
import warnings

import pygame

import grid as gol

pygame.init()

WIDTH = 1200
HEIGHT = 700
TITLE_HEIGHT = 60

ROWS = gol.ROWS
COLS = gol.COLS
CELL_SIZE = gol.CELL_SIZE
GRID_SIZE = gol.WINDOW_SIZE
GRID_X = WIDTH - GRID_SIZE - 30
GRID_Y = TITLE_HEIGHT + 20

LEFT_PANEL_X = 20
LEFT_PANEL_WIDTH = GRID_X - LEFT_PANEL_X - 20

BG_UI = (30, 30, 30)
TITLE_COLOR = (50, 50, 50)
PANEL_TEXT = (235, 235, 235)
BTN_START = (200, 0, 200)
BTN_PAUSE = (100, 0, 200)
BTN_RESET = (200, 0, 0)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Game of Life")
clock = pygame.time.Clock()

# Font backend selector:
# - Prefer pygame.font (normal behavior when available)
# - Fall back to pygame._freetype on Python/pygame combos where pygame.font is broken
_font_backend = "pygame"


class FreeTypeFontAdapter:
    def __init__(self, size):
        from pygame import _freetype

        if not _freetype.get_init():
            _freetype.init()
        self._font = _freetype.Font(None, size=max(1, size))
        self._font.pad = True
        self._font.kerning = False

    def render(self, text, antialias, color, background=None):
        if background is None:
            surface, _ = self._font.render(str(text), fgcolor=color)
        else:
            surface, _ = self._font.render(str(text), fgcolor=color, bgcolor=background)
        return surface

    def get_height(self):
        return int(math.ceil(self._font.get_sized_height()))


# use font and size for each parameter
def make_font(name, size):
    global _font_backend

    if _font_backend == "pygame":
        try:
            with warnings.catch_warnings():
                warnings.simplefilter("ignore", RuntimeWarning)
                return pygame.font.SysFont(name, size)
        except Exception:
            _font_backend = "freetype"

    return FreeTypeFontAdapter(size)

font_title = make_font("Times New Roman", 40)
font_button = make_font("Times New Roman", 28)
font_slider = make_font("Times New Roman", 24)
font_text = make_font("Times New Roman", 20)
font_status = make_font("Times New Roman", 24)

TEXT = (
    "Type :\n"
    "G : Glider\n"
    "B : Blinker\n"
    "P : Pulsar\n"
    "R : R-pentomino\n"
    "U : User configuration\n"
    "I : random initialisation\n"
    "\n"
    "Space : Play / Pause\n"
    "Mouse : toggle cell in pause/user mode")

BUTTON_WIDTH = 375
BUTTON_HEIGHT = 50
BUTTON_SPACING = 16
BUTTON_Y = HEIGHT - 80

start_button = pygame.Rect(LEFT_PANEL_X, BUTTON_Y, BUTTON_WIDTH, BUTTON_HEIGHT)
pause_button = pygame.Rect(start_button.right + BUTTON_SPACING, BUTTON_Y, BUTTON_WIDTH, BUTTON_HEIGHT)
reset_button = pygame.Rect(pause_button.right + BUTTON_SPACING, BUTTON_Y, BUTTON_WIDTH, BUTTON_HEIGHT)

SLIDER_HEIGHT = 36
slider = pygame.Rect(LEFT_PANEL_X, BUTTON_Y - 75, LEFT_PANEL_WIDTH, SLIDER_HEIGHT)
handle_radius = 10

MIN_SPEED = 1
MAX_SPEED = 60
speed = max(MIN_SPEED, min(MAX_SPEED, gol.FPS))
handle_x = slider.x + int((speed - MIN_SPEED) / (MAX_SPEED - MIN_SPEED) * slider.width)
dragging = False

GLIDER = [(0, 1), (1, 2), (2, 0), (2, 1), (2, 2)]
BLINKER = [(0, 0), (0, 1), (0, 2)]
R_PENTOMINO = [(0, 1), (0, 2), (1, 0), (1, 1), (2, 1)]
PULSAR_MAP = [
    ".............",
    "..***...***..",
    ".............",
    "*....*.*....*",
    "*....*.*....*",
    "*....*.*....*",
    "..***...***..",
    ".............",
    "..***...***..",
    "*....*.*....*",
    "*....*.*....*",
    "*....*.*....*",
    "..***...***..",
]


gol.reset_module_grid()
paused = True
user_mode = False
generation_timer = 0.0


def draw_multiline_text(text, x, y, font, color=PANEL_TEXT, line_spacing=4):
    lines = text.split("\n")
    for index, line in enumerate(lines):
        surface = font.render(line, True, color)
        screen.blit(surface, (x, y + index * (font.get_height() + line_spacing)))


def draw_title():
    pygame.draw.rect(screen, TITLE_COLOR, (0, 0, WIDTH, TITLE_HEIGHT))
    text = font_title.render("Game of Life", True, (255, 255, 255))
    screen.blit(text, text.get_rect(center=(WIDTH // 2, TITLE_HEIGHT // 2)))


def draw_buttons():
    pygame.draw.rect(screen, BTN_START, start_button)
    pygame.draw.rect(screen, BTN_PAUSE, pause_button)
    pygame.draw.rect(screen, BTN_RESET, reset_button)

    start_text = font_button.render("PLAY", True, (255, 255, 255))
    pause_text = font_button.render("PAUSE", True, (255, 255, 255))
    reset_text = font_button.render("RESET", True, (255, 255, 255))

    screen.blit(start_text, start_text.get_rect(center=start_button.center))
    screen.blit(pause_text, pause_text.get_rect(center=pause_button.center))
    screen.blit(reset_text, reset_text.get_rect(center=reset_button.center))


def draw_slider():
    slider_y = slider.y + slider.height // 2
    pygame.draw.line(
        screen,
        (255, 255, 255),
        (slider.x, slider_y),
        (slider.right, slider_y),
        5,
    )
    pygame.draw.circle(screen, (255, 128, 0), (handle_x, slider_y), handle_radius)
    label = font_slider.render(f"Speed: {speed} gen/s", True, (255, 170, 70))
    screen.blit(label, (slider.x, slider.y - 32))


def draw_status():
    if paused:
        state_text = "PAUSE"
    else:
        state_text = "RUN"

    if user_mode:
        state_text = "USER"

    live_cells = gol.count_live_cells(gol.grid, ROWS, COLS)
    status = f"State: {state_text}  |  Live cells: {live_cells}"
    surface = font_status.render(status, True, (235, 235, 235))
    screen.blit(surface, (LEFT_PANEL_X, GRID_Y + 270))


def draw_grid():
    gol.draw_grid(screen, gol.grid, ROWS, COLS, CELL_SIZE, GRID_X, GRID_Y)
    background_rect = pygame.Rect(GRID_X, GRID_Y, GRID_SIZE, GRID_SIZE)
    pygame.draw.rect(screen, (245, 245, 245), background_rect, 2)


def update_speed():
    global speed
    ratio = (handle_x - slider.x) / slider.width
    raw_speed = MIN_SPEED + ratio * (MAX_SPEED - MIN_SPEED)
    speed = max(MIN_SPEED, min(MAX_SPEED, int(round(raw_speed))))


def move_handle_to(mouse_x):
    global handle_x
    handle_x = max(slider.x, min(mouse_x, slider.right))
    update_speed()


def clear_grid():
    gol.clear_grid(gol.grid, ROWS, COLS)


def parse_pattern_map(pattern_map):
    coords = []
    for row, line in enumerate(pattern_map):
        for col, char in enumerate(line):
            if char == "*":
                coords.append((row, col))
    return coords


PULSAR = parse_pattern_map(PULSAR_MAP)


def place_pattern_center(pattern_coords):
    global user_mode
    gol.place_pattern_center(gol.grid, pattern_coords, ROWS, COLS)
    user_mode = False


def random_initialisation():
    global user_mode
    gol.clear_grid(gol.grid, ROWS, COLS)
    gol.randomize_grid(gol.grid, ROWS, COLS)
    user_mode = False


def point_in_grid(pos):
    x, y = pos
    return GRID_X <= x < GRID_X + GRID_SIZE and GRID_Y <= y < GRID_Y + GRID_SIZE


def toggle_cell_from_mouse(pos):
    x, y = pos
    col = (x - GRID_X) // CELL_SIZE
    row = (y - GRID_Y) // CELL_SIZE
    gol.toggle_cell(gol.grid, row, col, ROWS, COLS)


while True:
    dt = clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos

            if start_button.collidepoint(mouse_pos):
                paused = False
                user_mode = False
            elif pause_button.collidepoint(mouse_pos):
                paused = True
            elif reset_button.collidepoint(mouse_pos):
                clear_grid()
                paused = True
                user_mode = False
            elif slider.collidepoint(mouse_pos) or math.dist(
                mouse_pos, (handle_x, slider.y + slider.height // 2)
            ) <= handle_radius + 4:
                dragging = True
                move_handle_to(mouse_pos[0])
            elif point_in_grid(mouse_pos) and (paused or user_mode):
                toggle_cell_from_mouse(mouse_pos)

        elif event.type == pygame.MOUSEBUTTONUP:
            dragging = False

        elif event.type == pygame.MOUSEMOTION and dragging:
            move_handle_to(event.pos[0])

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                paused = not paused
                if not paused:
                    user_mode = False
            elif event.key == pygame.K_g:
                place_pattern_center(GLIDER)
                paused = True
            elif event.key == pygame.K_b:
                place_pattern_center(BLINKER)
                paused = True
            elif event.key == pygame.K_p:
                place_pattern_center(PULSAR)
                paused = True
            elif event.key == pygame.K_r:
                place_pattern_center(R_PENTOMINO)
                paused = True
            elif event.key == pygame.K_u:
                clear_grid()
                paused = True
                user_mode = True
            elif event.key == pygame.K_i:
                random_initialisation()
                paused = True

    if paused:
        generation_timer = 0.0
    else:
        generation_timer += dt
        step_interval = 1000.0 / max(speed, 1)
        while generation_timer >= step_interval:
            gol.grid = gol.next_generation(gol.grid, ROWS, COLS)
            generation_timer -= step_interval

    screen.fill(BG_UI)
    draw_title()
    draw_multiline_text(TEXT, LEFT_PANEL_X, GRID_Y, font_text)
    draw_status()
    draw_slider()
    draw_buttons()
    draw_grid()
    pygame.display.flip()
