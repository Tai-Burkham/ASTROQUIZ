"""
File: instructions_screen.py
Author: Calvin Leavy, Ahmed Krubally, Michelle Orru, Tailor Burkham

Description:
This displays the instructions for gameplay and waits for any input to
dismiss.

"""
import pygame
import settings as s

# Load the background image
background_image = pygame.image.load("assets/images/menubackground.jpg")
background_image = pygame.transform.scale(background_image, (s.WIDTH, s.HEIGHT))

def instructions_screen(screen):
    """
    Display the instructions screen.

    Args:
        screen: The Pygame display surface.

    Returns:
        None
    """

    # Loads background image
    screen.fill(s.WHITE)

    # Blit the background image onto the screen
    screen.blit(background_image, (0, 0))
    
    # Render and center the instruction text
    font = pygame.font.Font(None, 36)
    text_lines = [
        "INSTRUCTIONS:",
        "- Use the arrow keys to move the ship.",
        "- Press the spacebar to shoot lasers.",
        "- Press 'P' to pause the game.",
        "- Press 'Esc' to exit the game.",
        "- Answer questions correctly and gain points.",
        "Have fun and good luck!"
    ]

    # Render each line of text
    y_offset = 100
    for line in text_lines:
        text_surface = font.render(line, True, s.WHITE)
        text_rect = text_surface.get_rect(center=(s.WIDTH // 2, y_offset))
        screen.blit(text_surface, text_rect)
        y_offset += 40

    # Render the "Press any key to start" message
    start_text = font.render("Press any key to start", True, s.WHITE)
    start_rect = start_text.get_rect(center=(s.WIDTH // 2, s.HEIGHT - 100))
    screen.blit(start_text, start_rect)

    pygame.display.flip()

    # Wait for any key press or mouse click to continue
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                waiting = False
            elif event.type == pygame.QUIT:
                pygame.quit()

    # Clear the screen
    screen.fill(s.BLACK)
    pygame.display.flip()
