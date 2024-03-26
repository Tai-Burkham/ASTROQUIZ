import pygame
import textwrap
import settings as s

OUTLINE_COLOR = (0, 0, 0)
# Outlines text without box
def outline_text(screen, text, height, font, width=0) :
    text_outline = font.render(text, True, OUTLINE_COLOR)
    rendered_text = font.render(text, True, s.WHITE)

    screen.blit(text_outline, (s.WIDTH // 2 - text_outline.get_width() // 2 - 1 + width, height))
    screen.blit(text_outline, (s.WIDTH // 2 - text_outline.get_width() // 2 + 1 + width, height))
    screen.blit(text_outline, (s.WIDTH // 2 - text_outline.get_width() // 2 + width, height - 1))
    screen.blit(text_outline, (s.WIDTH // 2 - text_outline.get_width() // 2 + width, height + 1))
    screen.blit(rendered_text, (s.WIDTH // 2 - rendered_text.get_width() // 2 + width, height))

    button_rect = pygame.Rect(s.WIDTH // 2 - rendered_text.get_width() // 2 - 10 + width, height - 7, rendered_text.get_width() + 20, 40)

    return button_rect

def outline_text_w_box(screen, text, height, font, width = 0) :
    text_outline = font.render(text, True, OUTLINE_COLOR)
    rendered_text = font.render(text, True, s.WHITE)

    screen.blit(text_outline, (s.WIDTH // 2 - text_outline.get_width() // 2 - 1 + width, height))
    screen.blit(text_outline, (s.WIDTH // 2 - text_outline.get_width() // 2 + 1 + width, height))
    screen.blit(text_outline, (s.WIDTH // 2 - text_outline.get_width() // 2 + width, height - 1))
    screen.blit(text_outline, (s.WIDTH // 2 - text_outline.get_width() // 2 + width, height + 1))
    screen.blit(rendered_text, (s.WIDTH // 2 - rendered_text.get_width() // 2 + width, height))

    button_rect = pygame.Rect(s.WIDTH // 2 - rendered_text.get_width() // 2 - 10 + width, height - 7, rendered_text.get_width() + 20, 40)
    pygame.draw.rect(screen, (255, 255, 255, 0), button_rect, 1)

    return button_rect

def render_textrect(string, font, rect, text_color, background_color, justification=0):
    """Returns a surface containing the passed text, reformatted
    to fit within the given rect, word-wrapping as necessary.
    """
    final_lines = []
    requested_lines = string.splitlines()
    
    # Create a rectangle to contain the text
    surface = pygame.Surface(rect.size, pygame.SRCALPHA)
    # Break the text into lines that fit in the rectangle
    for requested_line in requested_lines:
        words = requested_line.split(' ')
        accumulated_line = ''
        for word in words:
            test_line = accumulated_line + ' ' + word if accumulated_line else word
            # Check if the test line fits in the rectangle
            if font.size(test_line)[0] < rect.width:
                accumulated_line = test_line
            else:
                final_lines.append(accumulated_line)
                accumulated_line = word
        final_lines.append(accumulated_line)

    # Render each line onto the surface
    y = 0  # Initialize y position
    for line in final_lines:
        if line:
            text_surface = font.render(line, True, text_color)
            # Position the text according to the justification argument
            if justification == 0:
                surface.blit(text_surface, (0, y))
            elif justification == 1:
                surface.blit(text_surface, ((rect.width - text_surface.get_width()) // 2, y))
            elif justification == 2:
                surface.blit(text_surface, (rect.width - text_surface.get_width(), y))
            # Increment y by the height of the rendered text
            y += text_surface.get_height()
    return surface