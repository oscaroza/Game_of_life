import math
import sys
import pygame
import grid as gol
import grid_persistence

pygame.init()
 
#size of the window
WIDTH = 1200
HEIGHT = 700
TITLE_HEIGHT = 60

#grid parameters
ROWS = gol.ROWS
COLS = gol.COLS
CELL_SIZE = gol.CELL_SIZE
GRID_SIZE = gol.WINDOW_SIZE
GRID_X = WIDTH - GRID_SIZE - 30
GRID_Y = TITLE_HEIGHT + 20

LEFT_PANEL_X = 20
LEFT_PANEL_WIDTH = GRID_X - LEFT_PANEL_X - 20

#Colors of the UI elements
BG_UI = (30, 30, 30)
TITLE_COLOR = (50, 50, 50)
PANEL_TEXT = (235, 235, 235)
BTN_START = (200, 0, 200)
BTN_PAUSE = (100, 0, 200)
BTN_RESET = (200, 0, 0)

#Set up the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Game of Life")
clock = pygame.time.Clock()

#Creates and returns a system font using pygame's font module
def make_font(name, size):
    return pygame.font.SysFont(name, size)

#Fonts for different UI elements
font_title = make_font("Times New Roman", 40)
font_button = make_font("Times New Roman", 28)
font_slider = make_font("Times New Roman", 24)
font_text = make_font("Times New Roman", 20)
font_status = make_font("Times New Roman", 24)

#Instructions for the user
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

#Button dimensions and positions
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

#Predefined patterns
GLIDER = [(0, 1), (1, 2), (2, 0), (2, 1), (2, 2)]
BLINKER = [(0, 0), (0, 1), (0, 2)]
R_PENTOMINO = [(0, 1), (0, 2), (1, 0), (1, 1), (2, 1)]
PULSAR = [
    (1, 2), (1, 3), (1, 4), (1, 8), (1, 9), (1, 10),
    (3, 0), (3, 5), (3, 7), (3, 12),
    (4, 0), (4, 5), (4, 7), (4, 12),
    (5, 0), (5, 5), (5, 7), (5, 12),
    (6, 2), (6, 3), (6, 4), (6, 8), (6, 9), (6, 10),
    (8, 2), (8, 3), (8, 4), (8, 8), (8, 9), (8, 10),
    (9, 0), (9, 5), (9, 7), (9, 12),
    (10, 0), (10, 5), (10, 7), (10, 12),
    (11, 0), (11, 5), (11, 7), (11, 12),
    (12, 2), (12, 3), (12, 4), (12, 8), (12, 9), (12, 10),]

#Place predefined patterns in the center of the grid
def place_pattern_center(pattern_coords):
    global user_mode
    gol.place_pattern_center(gol.grid, pattern_coords, ROWS, COLS)
    user_mode = False

#Randomly initialize the grid function
def random_initialisation():
    global user_mode
    gol.clear_grid(gol.grid, ROWS, COLS)
    gol.randomize_grid(gol.grid, ROWS, COLS)
    user_mode = False

#Initialize the grid and state variables
gol.reset_module_grid()
paused = True
user_mode = False
generation_timer = 0.0

# Saves the current state of the grid (live cells) to persistent storage
def save_current_grid_state():
    grid_persistence.save_live_cells(gol.grid, ROWS, COLS)
 
#Load the saved grid state
grid_persistence.load_live_cells(gol.grid, ROWS, COLS)
grid_persistence.register_auto_save(save_current_grid_state)


#Functions to draw UI elements and handle interactions
def draw_text(text, x, y, font, color=PANEL_TEXT, line_spacing=4):
    lines = text.split("\n")
    for index, line in enumerate(lines):
        surface = font.render(line, True, color)
        screen.blit(surface, (x, y + index * (font.get_height() + line_spacing)))

#Title bar function
def draw_title():
    pygame.draw.rect(screen, TITLE_COLOR, (0, 0, WIDTH, TITLE_HEIGHT)) #position, size of the rectangle
    text = font_title.render("Game of Life", True, (255, 255, 255)) #color of the text 
    screen.blit(text, text.get_rect(center=(WIDTH // 2, TITLE_HEIGHT // 2))) #position the text in the center of the title bar

#Control buttons function
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

#Speed slider function
def draw_slider():
    slider_y = slider.y + slider.height // 2
    pygame.draw.line(
        screen,
        (255, 255, 255),
        (slider.x, slider_y),
        (slider.right, slider_y),
        5, )
    pygame.draw.circle(screen, (255, 128, 0), (handle_x, slider_y), handle_radius)
    label = font_slider.render(f"Speed: {speed} gen/s", True, (255, 170, 70))
    screen.blit(label, (slider.x, slider.y - 32))

#Status display function
def draw_status():
    if paused:
        state_text = "PAUSE"
    else:
        state_text = "RUN"

    if user_mode:
        state_text = "USER"

    live_cells = gol.count_live_cells(gol.grid, ROWS, COLS) #Count live cells in the grid
    status = f"State: {state_text}  |  Live cells: {live_cells}"
 #Display the status text
    surface = font_status.render(status, True, (235, 235, 235))
    screen.blit(surface, (LEFT_PANEL_X, GRID_Y + 270))

#Grid drawing function
def draw_grid():
    gol.draw_grid(screen, gol.grid, ROWS, COLS, CELL_SIZE, GRID_X, GRID_Y)
    background_rect = pygame.Rect(GRID_X, GRID_Y, GRID_SIZE, GRID_SIZE)
    pygame.draw.rect(screen, (245, 245, 245), background_rect, 2)

#Update speed based on slider position
def update_speed():
    global speed
    ratio = (handle_x - slider.x) / slider.width
    raw_speed = MIN_SPEED + ratio * (MAX_SPEED - MIN_SPEED)
    speed = max(MIN_SPEED, min(MAX_SPEED, int(round(raw_speed))))

#Move the slider handle to the mouse position while dragging
def move_slider(x):
    global handle_x
    handle_x = max(slider.x, min(slider.right, x))
    update_speed()

#Toggles a cell state (alive/dead) based on mouse position
def toggle_cell_from_mouse(mouse_pos):
    if not (paused or user_mode):
        return
    mouse_x, mouse_y = mouse_pos
    if not (GRID_X <= mouse_x < GRID_X + GRID_SIZE and GRID_Y <= mouse_y < GRID_Y + GRID_SIZE):
        return

 #Convert mouse position to grid coordinates
    grid_col = (mouse_x - GRID_X) // CELL_SIZE
    grid_row = (mouse_y - GRID_Y) // CELL_SIZE
    gol.toggle_cell(gol.grid, grid_row, grid_col, ROWS, COLS)     #Toggle the selected cell state


#Clear the grid function
def clear_grid():
    gol.clear_grid(gol.grid, ROWS, COLS)

while True:
    dt = clock.tick(60)

    for event in pygame.event.get(): 
        if event.type == pygame.QUIT: #if the user clicks the close button, quit pygame and exit the program
            save_current_grid_state()
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN: #if the user clicks the mouse, check what button is it and respond accordingly
            mouse_pos = event.pos

            if start_button.collidepoint(mouse_pos): #"Play" button, unpause the game and disable user mode
                paused = False
                user_mode = False
            elif pause_button.collidepoint(mouse_pos): #"Pause" button, pause the game
                paused = True
            elif reset_button.collidepoint(mouse_pos): #"Reset" button, clear the grid, pause the game and disable user mode
                clear_grid()
                paused = True
                user_mode = False
            elif slider.collidepoint(event.pos):
                dragging = True
                move_slider(mouse_pos[0]) #Move the slider handle to the mouse position
            else:
                toggle_cell_from_mouse(mouse_pos)

        elif event.type == pygame.MOUSEBUTTONUP:
            dragging = False
         
#While dragging, continuously update slider position
        elif event.type == pygame.MOUSEMOTION and dragging: 
            move_slider(event.pos[0])

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE: #if the user presses the "Space", toggle between play and pause
                paused = not paused
                if not paused:
                    user_mode = False
            elif event.key == pygame.K_g: #if the user presses the "G", grid pause + the Glider pattern
                place_pattern_center(GLIDER)
                paused = True
            elif event.key == pygame.K_b: #if the user presses the "B", grid pause + the Blinker pattern
                place_pattern_center(BLINKER)
                paused = True
            elif event.key == pygame.K_p: #if the user presses the "P", grid pause + the Pulsar pattern
                place_pattern_center(PULSAR)
                paused = True
            elif event.key == pygame.K_r: #if the user presses the "R", grid pause + the R-pentomino pattern 
                place_pattern_center(R_PENTOMINO)
                paused = True
            elif event.key == pygame.K_u: #if the user presses the "U", grid pause, cleared + the user can create their own configuration
                clear_grid()
                paused = True
                user_mode = True
            elif event.key == pygame.K_i: #if the user presses the "I", grid pause + randomly initialized
                random_initialisation()
                paused = True

#Update the grid to the next generation based on the current speed if the game is not paused
    if paused:
        generation_timer = 0.0
    else:
        generation_timer += dt
        step_interval = 1000 / max(speed, 1)
        
        if generation_timer >= step_interval:
            gol.grid = gol.next_generation(gol.grid, ROWS, COLS)
            generation_timer -= step_interval

#Show the functions to draw the UI elements and update the display
    screen.fill(BG_UI)
    draw_title()
    draw_text(TEXT, LEFT_PANEL_X, GRID_Y, font_text)
    draw_status()
    draw_slider()
    draw_buttons()
    draw_grid()
    pygame.display.flip()
