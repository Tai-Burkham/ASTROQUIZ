"""
File: utilities.py
Author: Calvin Leavy, Ahmed Krubally, Michelle Orro, Tailor Burkham

Description:
Utility functions for the game, including text wrapping and rendering.

"""
import pygame
import settings as s

# Global variable for text outline color
OUTLINE_COLOR = (0, 0, 0)

# Outlines text without box
def outline_text(screen, text, height, font, width=0):
    """
    Renders text with an outline effect without a box.
    
    Args:
        screen: The Pygame surface to render the text onto.
        text: The text to render.
        height: The vertical position of the text.
        font: The Pygame font to use for rendering.
        width: Optional horizontal offset for positioning.
        
    Returns:
        button_rect: The rectangle representing the area covered by the text.
    """

    # Render the text
    text_outline = font.render(text, True, OUTLINE_COLOR)
    rendered_text = font.render(text, True, s.WHITE)

    # Blit the text to the screen with an outline effect
    screen.blit(text_outline, (s.WIDTH // 2 - text_outline.get_width() // 2 - 1 + width, height))
    screen.blit(text_outline, (s.WIDTH // 2 - text_outline.get_width() // 2 + 1 + width, height))
    screen.blit(text_outline, (s.WIDTH // 2 - text_outline.get_width() // 2 + width, height - 1))
    screen.blit(text_outline, (s.WIDTH // 2 - text_outline.get_width() // 2 + width, height + 1))
    screen.blit(rendered_text, (s.WIDTH // 2 - rendered_text.get_width() // 2 + width, height))

    # Create a rect for the button
    button_rect = pygame.Rect(s.WIDTH // 2 - rendered_text.get_width() // 2 - 10 + width, height - 7, rendered_text.get_width() + 20, 40)

    return button_rect

# Outlines text with box
def outline_text_w_box(screen, text, height, font, width = 0):
    """
    Renders text with an outline effect and a surrounding box.
    
    Args:
        screen: The Pygame surface to render the text onto.
        text: The text to render.
        height: The vertical position of the text.
        font: The Pygame font to use for rendering.
        width: Optional horizontal offset for positioning.
        
    Returns:
        button_rect: The rectangle representing the area covered by the text.
    """

    # Render the text
    text_outline = font.render(text, True, OUTLINE_COLOR)
    rendered_text = font.render(text, True, s.WHITE)

    # Blit the text to the screen with an outline effect
    screen.blit(text_outline, (s.WIDTH // 2 - text_outline.get_width() // 2 - 1 + width, height))
    screen.blit(text_outline, (s.WIDTH // 2 - text_outline.get_width() // 2 + 1 + width, height))
    screen.blit(text_outline, (s.WIDTH // 2 - text_outline.get_width() // 2 + width, height - 1))
    screen.blit(text_outline, (s.WIDTH // 2 - text_outline.get_width() // 2 + width, height + 1))
    screen.blit(rendered_text, (s.WIDTH // 2 - rendered_text.get_width() // 2 + width, height))

    # Create a rect for the button
    button_rect = pygame.Rect(s.WIDTH // 2 - rendered_text.get_width() // 2 - 10 + width, height - 7, rendered_text.get_width() + 20, 40)
    
    # Draw a rectangle around the text
    pygame.draw.rect(screen, (255, 255, 255, 0), button_rect, 1)

    return button_rect

# Wraps text
def render_textrect(string, font, rect, text_color, background_color, justification=0):
    """
    Renders text within a given rectangle, wrapping as necessary.
    
    Args:
        string: The text string to render.
        font: The Pygame font to use for rendering.
        rect: The rectangle representing the area to render the text within.
        text_color: The color of the text.
        background_color: The background color behind the text.
        justification: The justification of the text within the rectangle (0=left, 1=center, 2=right).
        
    Returns:
        surface: The Pygame surface containing the rendered text.
    """

    # Remove any leading or trailing newlines from the string
    final_lines = []
    requested_lines = string.splitlines()
    
    # Create a rectangle to contain the text
    surface = pygame.Surface(rect.size, pygame.SRCALPHA)

    # Break the text into lines that fit within the rectangle
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
    y = 0
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
            y += text_surface.get_height()
    return surface