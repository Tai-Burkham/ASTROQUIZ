import pygame
import game

pygame.init()

# Window size and colors
WIDTH, HEIGHT = 900, 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
FONT = pygame.font.Font(None, 36)
TEXT_COLOR = (255, 255, 255)
OUTLINE_COLOR = (0, 0, 0)

# we will run the questions from a seperate json file later when implementing the edit question screen
questions = [
    "This is question 1.",
    "This is question 2.",
    "This is question 3.",
    # Add more questions as needed
]

# Initializes the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("ASTROQUIZ")

background_image = pygame.image.load("Game Files/assets/images/menubackground.jpg")
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))

button_rect = pygame.Rect(WIDTH // 2 - 50, HEIGHT // 2 - 24, 100, 50)

def outline_text(text, height) :
    text_outline = FONT.render(text, True, OUTLINE_COLOR)
    rendered_text = FONT.render(text, True, WHITE)

    screen.blit(text_outline, (WIDTH // 2 - text_outline.get_width() // 2 - 1, height))
    screen.blit(text_outline, (WIDTH // 2 - text_outline.get_width() // 2 + 1, height))
    screen.blit(text_outline, (WIDTH // 2 - text_outline.get_width() // 2, height - 1))
    screen.blit(text_outline, (WIDTH // 2 - text_outline.get_width() // 2, height + 1))
    screen.blit(rendered_text, (WIDTH // 2 - rendered_text.get_width() // 2, height))

    button_rect = pygame.Rect(WIDTH // 2 - rendered_text.get_width() // 2 - 10, height - 7, rendered_text.get_width() + 20, 40)
    pygame.draw.rect(screen, (255, 255, 255, 0), button_rect, 2)


# We can make this clickable once we have the design of the menu page more complete
def main_menu():
    # Display main menu options
    screen.fill(WHITE)
    screen.blit(background_image, (0, 0))

    # The game title needs to be drawn on the menu image so it will not look like this when done
    outline_text("ASTROQUIZ", 100)
    
    outline_text("Play Game (Press 'P')", 200)

    outline_text("High Scores (Press 'H')", 250)

    outline_text("Edit Questions (Press 'E')", 300)
    
    outline_text("Edit Settings (Press 'S')", 350)

    outline_text("Quit (Press 'Q')", 400)
    
    pygame.display.flip()

def main():
    running = True
    while running:
        main_menu()

        # Once we have the menu design complete we can change from pushing buttons for menu items to clickon on them with the mouse
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    game.game(screen)
                elif event.key == pygame.K_h:
                    # Show high scores
                    pass
                elif event.key == pygame.K_e:
                    # Edit questions
                    pass
                elif event.key == pygame.K_s:
                    # Edit settings
                    pass
                elif event.key == pygame.K_q:
                    pygame.quit()

    pygame.quit()

if __name__ == "__main__":
    main()