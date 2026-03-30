from pathlib import Path
import warnings

import pygame


def _load_image_surface(image_path):
    try:
        return pygame.image.load(str(image_path))
    except pygame.error:
        from PIL import Image

        with Image.open(image_path) as pil_img:
            pil_img = pil_img.convert("RGB")
            raw_bytes = pil_img.tobytes()
            size = pil_img.size

        return pygame.image.fromstring(raw_bytes, size, "RGB")


def _render_text(text, color, size=50):
    try:
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", RuntimeWarning)
            font = pygame.font.SysFont("Times New Roman", size)
        return font.render(text, True, color)
    except Exception:
        from pygame import _freetype

        _freetype.init()
        fallback_font = _freetype.Font(None, size)
        surface, _ = fallback_font.render(text or "", fgcolor=color)
        return surface


def show_welcome(image_name="Welcome.jpg", duration_seconds=5, caption="Game of Life"):
    """Affiche un écran d'accueil pendant `duration_seconds`, puis rend la main."""
    pygame.init()

    base_dir = Path(__file__).resolve().parent
    image_path = base_dir / image_name

    image = _load_image_surface(image_path)
    width, height = image.get_size()

    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption(caption)
    image = image.convert()

    clock = pygame.time.Clock()
    text = "Continue>>"

    text_surface = _render_text(text, (200, 0, 200), size=50)
    text_rect = text_surface.get_rect()
    text_rect.x = min(1200, width - text_rect.width - 10)
    text_rect.y = height - text_rect.height - 50

    background_rect = text_rect.inflate(20, 25)

    start_ticks = pygame.time.get_ticks()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False

        elapsed_ms = pygame.time.get_ticks() - start_ticks
        if elapsed_ms >= duration_seconds * 1000:
            pygame.display.quit()
            return True

        screen.blit(image, (0, 0))
        pygame.draw.rect(screen, (255, 255, 255), background_rect)
        screen.blit(text_surface, text_rect)
        pygame.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    show_welcome()
