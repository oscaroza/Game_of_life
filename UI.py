#design the user interface for a 506x506 game window
import pygame 
import sys 

pygame.init()

# Taille de la fenêtre 
WIDTH = 1200
HEIGHT = 700

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Game of Life")

#zones
TITLE_HEIGHT = 60
BOTTOM_HEIGHT = 120
GRID_SIZE = 506
GRID_X = (WIDTH - GRID_SIZE) // 2
GRID_Y = TITLE_HEIGHT + 20

# Couleurs
COLOR = (30, 30, 30)    
TITLE_COLOR = (50, 50, 50)


#Font
font_title = pygame.font.SysFont("Times New Roman", 40)
font_button = pygame.font.SysFont("Times New Roman", 30)

# Buttons for controlling the game
BUTTON_WIDTH = 300
BUTTON_HEIGHT = 50
BUTTON_Y = HEIGHT - 80

start_button = pygame.Rect(0, 0, BUTTON_WIDTH, BUTTON_HEIGHT)
pause_button = pygame.Rect(0, 0, BUTTON_WIDTH, BUTTON_HEIGHT)
reset_button = pygame.Rect(0, 0, BUTTON_WIDTH, BUTTON_HEIGHT)
spacing = 40

total_width = BUTTON_WIDTH * 3 + spacing * 2
start_button.x = (WIDTH - total_width) // 2
pause_button.x = start_button.x + BUTTON_WIDTH + spacing
reset_button.x = pause_button.x + BUTTON_WIDTH + spacing

start_button.y = pause_button.y = reset_button.y = BUTTON_Y

#title 
def draw_title():
    pygame.draw.rect(screen, TITLE_COLOR, (0, 0, WIDTH, TITLE_HEIGHT))
    text = font_title.render("Game of Life", True, (255, 255, 255))
    text_rect = text.get_rect(center=(WIDTH // 2, TITLE_HEIGHT // 2))
    screen.blit(text, text_rect)

#buttons
def draw_buttons():
    pygame.draw.rect(screen, (200,0,200), start_button)
    pygame.draw.rect(screen, (100,0,200), pause_button)
    pygame.draw.rect(screen, (200,0,0), reset_button)

def buttons_start():
    text = font_title.render("START", True, (255, 255, 255))
    text_rect = text.get_rect(center=(start_button.x + BUTTON_WIDTH // 2, start_button.y + BUTTON_HEIGHT // 2))
    screen.blit(text, text_rect)

def buttons_pause():
    text = font_title.render("PAUSE", True, (255, 255, 255))
    text_rect = text.get_rect(center=(pause_button.x + BUTTON_WIDTH // 2, pause_button.y + BUTTON_HEIGHT // 2))
    screen.blit(text, text_rect)

def buttons_reset():
    text = font_title.render("RESET", True, (255, 255, 255))
    text_rect = text.get_rect(center=(reset_button.x + BUTTON_WIDTH // 2, reset_button.y + BUTTON_HEIGHT // 2))
    screen.blit(text, text_rect)

running = True
clock = pygame.time.Clock()

while running:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(COLOR)
    draw_title()
    draw_buttons()
    buttons_start()
    buttons_pause()
    buttons_reset()

    pygame.display.flip()
