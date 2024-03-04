import pygame
import random
import game

pygame.init()

# Window size and colors
WIDTH, HEIGHT = 1200, 800
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
FONT = pygame.font.Font(None, 36)

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

def main_menu():
    # Display main menu options
    screen.fill(WHITE)
    text = FONT.render("ASTROQUIZ", True, BLACK)
    screen.blit(text, (WIDTH // 2 - text.get_width() // 2, 100))
    
    play_text = FONT.render("Play Game (Press 'P')", True, BLACK)
    screen.blit(play_text, (WIDTH // 2 - play_text.get_width() // 2, 200))
    
    high_scores_text = FONT.render("High Scores (Press 'H')", True, BLACK)
    screen.blit(high_scores_text, (WIDTH // 2 - high_scores_text.get_width() // 2, 250))
    
    edit_questions_text = FONT.render("Edit Questions (Press 'E')", True, BLACK)
    screen.blit(edit_questions_text, (WIDTH // 2 - edit_questions_text.get_width() // 2, 300))

    edit_questions_text = FONT.render("Edit Settings (Press 'S')", True, BLACK)
    screen.blit(edit_questions_text, (WIDTH // 2 - edit_questions_text.get_width() // 2, 350))

    edit_questions_text = FONT.render("Quit (Press 'Q')", True, BLACK)
    screen.blit(edit_questions_text, (WIDTH // 2 - edit_questions_text.get_width() // 2, 400))
    
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