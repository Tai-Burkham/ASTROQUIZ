import pygame
import settings as s

OUTLINE_COLOR = (0, 0, 0)
# Outlines text without box
def outline_text(screen, text, height) :
    text_outline = s.FONT.render(text, True, OUTLINE_COLOR)
    rendered_text = s.FONT.render(text, True, s.WHITE)

    screen.blit(text_outline, (s.WIDTH // 2 - text_outline.get_width() // 2 - 1, height))
    screen.blit(text_outline, (s.WIDTH // 2 - text_outline.get_width() // 2 + 1, height))
    screen.blit(text_outline, (s.WIDTH // 2 - text_outline.get_width() // 2, height - 1))
    screen.blit(text_outline, (s.WIDTH // 2 - text_outline.get_width() // 2, height + 1))
    screen.blit(rendered_text, (s.WIDTH // 2 - rendered_text.get_width() // 2, height))

def outline_text_w_box(screen, text, height, width=0) :
    text_outline = s.FONT.render(text, True, OUTLINE_COLOR)
    rendered_text = s.FONT.render(text, True, s.WHITE)

    screen.blit(text_outline, (s.WIDTH // 2 - text_outline.get_width() // 2 - 1 + width, height))
    screen.blit(text_outline, (s.WIDTH // 2 - text_outline.get_width() // 2 + 1 + width, height))
    screen.blit(text_outline, (s.WIDTH // 2 - text_outline.get_width() // 2 + width, height - 1))
    screen.blit(text_outline, (s.WIDTH // 2 - text_outline.get_width() // 2 + width, height + 1))
    screen.blit(rendered_text, (s.WIDTH // 2 - rendered_text.get_width() // 2 + width, height))

    button_rect = pygame.Rect(s.WIDTH // 2 - rendered_text.get_width() // 2 - 10 + width, height - 7, rendered_text.get_width() + 20, 40)
    pygame.draw.rect(screen, (255, 255, 255, 0), button_rect, 1)

    return button_rect