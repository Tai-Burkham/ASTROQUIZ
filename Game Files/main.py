import pygame
import game
import edit_questions
import settings
import high_scores
import settings as s
import utilities as u

pygame.init()

# Initializes the screen
screen = pygame.display.set_mode((s.WIDTH, s.HEIGHT))
pygame.display.set_caption("ASTROQUIZ")

# for the top left icon. Still need an icon image before implimenting
icon_image = pygame.image.load("Game Files/assets/images/Asteroid_3.png")
pygame.display.set_icon(icon_image)

# loads background image
background_image = pygame.image.load("Game Files/assets/images/menubackground_title.jpg")
background_image = pygame.transform.scale(background_image, (s.WIDTH, s.HEIGHT))

# Displays the menu items and returns the clickable boxes
def main_menu():
    # Display main menu options
    screen.fill(s.WHITE)
    screen.blit(background_image, (0, 0))
    
    # Creates menu buttons
    play_button_rect = u.outline_text_w_box(screen, "Play Game", 250, s.FONT)
    high_scores_button_rect = u.outline_text_w_box(screen, "High Scores", 300, s.FONT)
    edit_questions_button_rect = u.outline_text_w_box(screen, "Edit Questions", 350, s.FONT)    
    edit_settings_button_rect = u.outline_text_w_box(screen, "Edit Settings", 400, s.FONT)
    quit_button_rect = u.outline_text_w_box(screen, "Quit", 450, s.FONT) 

    pygame.display.flip()

    return play_button_rect, high_scores_button_rect, edit_questions_button_rect, edit_settings_button_rect, quit_button_rect

def main():
    running = True
    while running:
        play_button_rect, high_scores_button_rect, edit_questions_button_rect, edit_settings_button_rect, quit_button_rect = main_menu()

        # Once we have the menu design complete we can change from pushing buttons for menu items to clickon on them with the mouse
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            # We can remove the keyboard shortcuts for the menu at any time
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    game.game(screen)
                elif event.key == pygame.K_h:
                    # Show high scores
                    pass
                elif event.key == pygame.K_e:
                    edit_questions(screen)
                    pass
                elif event.key == pygame.K_s:
                    # Edit settings
                    pass
                elif event.key == pygame.K_q:
                    pygame.quit()
            # Makes menu choices clickable
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if play_button_rect.collidepoint(event.pos):
                    game.game(screen)
                elif high_scores_button_rect.collidepoint(event.pos):
                    high_scores.view_high_score(screen)
                elif edit_questions_button_rect.collidepoint(event.pos):
                    edit_questions.edit_questions(screen)
                elif edit_settings_button_rect.collidepoint(event.pos):
                    settings.edit_settings(screen)
                elif quit_button_rect.collidepoint(event.pos):
                    pygame.quit()

    pygame.quit()

if __name__ == "__main__":
    main()