"""
File: main.py
Author: Calvin Leavy, Ahmed Krubally, Michelle Orro, Tailor Burkham

Description:
This file serves as the main entry point for the ASTROQUIZ game.
It handles the initialization of Pygame, displays the main menu,
and handles user interactions for starting the game, accessing
high scores, editing questions, modifying settings, and quitting
the game.

"""
import pygame
import game
import edit_questions
import settings
import high_scores
import settings as s
import utilities as u
import instructions_screen 

# Initialize Pygame
pygame.init()

# Initialize the game window
screen = pygame.display.set_mode((s.WIDTH, s.HEIGHT))
pygame.display.set_caption("ASTROQUIZ")

# Load and set the window icon
icon_image = pygame.image.load("Game Files/assets/images/Asteroid_3.png")
pygame.display.set_icon(icon_image)

# Load and scale the background image
background_image = pygame.image.load("Game Files/assets/images/menubackground_title.jpg")
background_image = pygame.transform.scale(background_image, (s.WIDTH, s.HEIGHT))

# Function to display the main menu and return clickable boxes
def main_menu():
    # Display the background image
    screen.fill(s.WHITE)
    screen.blit(background_image, (0, 0))
    
    # Create menu buttons and get their rectangles
    play_button_rect = u.outline_text_w_box(screen, "Play Game", 250, s.FONT)
    high_scores_button_rect = u.outline_text_w_box(screen, "High Scores", 300, s.FONT)
    edit_questions_button_rect = u.outline_text_w_box(screen, "Edit Questions", 350, s.FONT)    
    edit_settings_button_rect = u.outline_text_w_box(screen, "Edit Settings", 400, s.FONT)
    quit_button_rect = u.outline_text_w_box(screen, "Quit", 450, s.FONT) 

    # Update the display
    pygame.display.flip()

    return play_button_rect, high_scores_button_rect, edit_questions_button_rect, edit_settings_button_rect, quit_button_rect

def main():
    running = True
    while running:
        # Get menu button rectangles
        play_button_rect, high_scores_button_rect, edit_questions_button_rect, edit_settings_button_rect, quit_button_rect = main_menu()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # Quit the game if the window close button is clicked
                running = False
            # Keyboard shortcuts for menu items
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    game.game(screen)
                elif event.key == pygame.K_h:
                    high_scores.view_high_score(screen)
                elif event.key == pygame.K_e:
                    edit_questions.edit_questions(screen)
                elif event.key == pygame.K_s:
                    settings.edit_settings(screen)
                elif event.key == pygame.K_q:
                    pygame.quit()
            # Handle mouse clicks on menu items 
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if play_button_rect.collidepoint(event.pos):
                    instructions_screen.instructions_screen(screen)
                    game.game(screen)
                elif high_scores_button_rect.collidepoint(event.pos):
                    high_scores.view_high_score(screen)
                elif edit_questions_button_rect.collidepoint(event.pos):
                    edit_questions.edit_questions(screen)
                elif edit_settings_button_rect.collidepoint(event.pos):
                    settings.edit_settings(screen)
                elif quit_button_rect.collidepoint(event.pos):
                    pygame.quit()

    # Quit Pygame when the main loop exits
    pygame.quit()   

if __name__ == "__main__":
    # Call the main function when the script is executed
    main()