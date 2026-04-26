from pathlib import Path
import pygame

def show_welcome(image_name="Welcome.jpg", duration_seconds=3):
    pygame.init()
    
#Load the image from disk
    base_dir = Path(__file__).resolve().parent
    image_path = base_dir / image_name     
    image = pygame.image.load(str(image_path))
    width, height = image.get_size()
    
#Size of the window 
    screen = pygame.display.set_mode((width, height))
    image = image.convert()

    start_ticks = pygame.time.get_ticks()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False
                
#check when the duration is passed (x1000 for ms to s)
        if pygame.time.get_ticks() - start_ticks >= duration_seconds * 1000:
            pygame.display.quit()
            return True

        screen.blit(image, (0, 0))
        pygame.display.flip()
