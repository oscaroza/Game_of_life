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


def show_welcome(image_name="Welcome.jpg", duration_seconds=3, caption="Game of Life"):
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
    label_surface = _render_text("Launching game", (40, 40, 40), size=40)
    line_y = height - label_surface.get_height() - 50
    right_margin = 30

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

        remaining_seconds = max(0.0, duration_seconds - (elapsed_ms / 1000.0))
        timer_surface = _render_text(f"{remaining_seconds:.1f}s", (200, 0, 200), size=40)
        timer_rect = timer_surface.get_rect(right=width - right_margin, y=line_y)
        label_rect = label_surface.get_rect(right=timer_rect.left - 16, y=line_y)
        content_rect = label_rect.union(timer_rect).inflate(20, 16)

        screen.blit(image, (0, 0))
        pygame.draw.rect(screen, (255, 255, 255), content_rect)
        screen.blit(label_surface, label_rect)
        screen.blit(timer_surface, timer_rect)
        pygame.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    show_welcome()
