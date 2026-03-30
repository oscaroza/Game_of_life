import pygame 
import sys 
import warnings

pygame.init()

# Taille de la fenêtre 
WIDTH = 1200
HEIGHT = 700

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Game of Life")
clock = pygame.time.Clock()

#zones
TITLE_HEIGHT = 60
GRID_SIZE = 506
GRID_X = (WIDTH - GRID_SIZE) // 2
GRID_Y = TITLE_HEIGHT + 20

# Couleurs
COLOR = (30, 30, 30)    
TITLE_COLOR = (50, 50, 50)

class FreetypeFontAdapter:
    def __init__(self, size):
        from pygame import _freetype
        _freetype.init()
        self._font = _freetype.Font(None, size)

    def render(self, text, antialias, color):
        surface, _ = self._font.render(text or "", fgcolor=color)
        return surface

    def get_height(self):
        return int(self._font.get_sized_height())


_font_fallback_warned = False


def make_font(name, size):
    global _font_fallback_warned
    try:
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", RuntimeWarning)
            return pygame.font.SysFont(name, size)
    except Exception as exc:
        if not _font_fallback_warned:
            print(
                "Warning: pygame.font unavailable, fallback to built-in freetype font "
                f"({exc})."
            )
            _font_fallback_warned = True
        return FreetypeFontAdapter(size)


# Font
font_title = make_font("Times New Roman", 40)
font_button = make_font("Times New Roman", 30)
font_slider = make_font("Times New Roman", 25)
font_text = make_font("Times New Roman", 20)

def draw_multiline_text(text, x, y, font, color=(255,255,255), line_spacing=5):
    lines = text.split("\n")  
    for i, line in enumerate(lines):
        surface = font.render(line, True, color)
        screen.blit(surface, (x, y + i * (font.get_height() + line_spacing)))

# Buttons
BUTTON_WIDTH = 250
BUTTON_HEIGHT = 50
BUTTON_Y = HEIGHT - 80

start_button = pygame.Rect(0, 0, BUTTON_WIDTH, BUTTON_HEIGHT)
pause_button = pygame.Rect(0, 0, BUTTON_WIDTH, BUTTON_HEIGHT)
reset_button = pygame.Rect(0, 0, BUTTON_WIDTH, BUTTON_HEIGHT)
slider = pygame.Rect(0, 0, BUTTON_WIDTH, BUTTON_HEIGHT) 

spacing = 35

total_width = BUTTON_WIDTH * 4 + spacing * 3
start_button.x = (WIDTH - total_width) // 3
pause_button.x = start_button.x + BUTTON_WIDTH + spacing
reset_button.x = pause_button.x + BUTTON_WIDTH + spacing
slider.x = reset_button.x + BUTTON_WIDTH + spacing

start_button.y = pause_button.y = reset_button.y = slider.y = BUTTON_Y

# Slider
handle_radius = 10
handle_x = slider.x + BUTTON_WIDTH // 2
dragging = False
speed = 50
top_left_text = "type G for Glider \n B : Blinker \n P : Pulsar \n R : R-pentomino \n U : User configuration \n I : random initialisation" 

#Functions
def draw_title():
    pygame.draw.rect(screen, TITLE_COLOR, (0, 0, WIDTH, TITLE_HEIGHT))
    text = font_title.render("Game of Life", True, (255, 255, 255))
    screen.blit(text, text.get_rect(center=(WIDTH // 2, TITLE_HEIGHT // 2)))

def draw_top_left_text():
    draw_multiline_text(top_left_text, 10, 65, font_text)

def draw_buttons():
    pygame.draw.rect(screen, (200,0,200), start_button)
    pygame.draw.rect(screen, (100,0,200), pause_button)
    pygame.draw.rect(screen, (200,0,0), reset_button)

def buttons_start():
    text = font_title.render("START", True, (255, 255, 255))
    screen.blit(text, text.get_rect(center=start_button.center))

def buttons_pause():
    text = font_title.render("PAUSE", True, (255, 255, 255))
    screen.blit(text, text.get_rect(center=pause_button.center))

def buttons_reset():
    text = font_title.render("RESET", True, (255, 255, 255))
    screen.blit(text, text.get_rect(center=reset_button.center))

def draw_slider():
    pygame.draw.rect(screen, (255, 255, 255), (slider.x, slider.y + BUTTON_HEIGHT//2, BUTTON_WIDTH, 5))
    pygame.draw.circle(screen, (255,128,0), (handle_x, slider.y + BUTTON_HEIGHT // 2), handle_radius)
    text = font_slider.render(f"Speed: {speed}", True, (255,128,0))
    screen.blit(text, (slider.x, slider.y - 10))

def update_speed():
    global speed
    ratio = (handle_x - slider.x) / BUTTON_WIDTH
    speed = int(ratio * 100)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        elif event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = pygame.mouse.get_pos()
            if abs(mx - handle_x) < handle_radius and abs(my - (slider.y + BUTTON_HEIGHT//2)) < 20:
                dragging = True
        elif event.type == pygame.MOUSEBUTTONUP:
            dragging = False

        elif event.type == pygame.MOUSEMOTION:
            if dragging:
                mx, _ = pygame.mouse.get_pos()
                handle_x = max(slider.x, min(mx, slider.x + BUTTON_WIDTH))
                update_speed()
    # Affichage
    screen.fill(COLOR)
    draw_title()
    draw_top_left_text()
    draw_buttons()
    buttons_start()
    buttons_pause()
    buttons_reset()
    draw_slider()

    pygame.display.flip()
    clock.tick(60)
