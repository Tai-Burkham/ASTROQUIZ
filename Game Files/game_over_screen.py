import pygame
import settings as s
import utilities as u

def game_over_screen(screen, score):
    # Clear the asteroid group
    

    # Create clickable boxes
    button_width = 180
    button_height = 50  # Adjusted height for smaller buttons
    button_spacing = 20

    # Define the dimensions of the black box
    box_width = 2 * button_width + button_spacing
    box_height = 3 * button_height  # Adjusted height for two buttons
    game_over_box = pygame.Rect((screen.get_width() - box_width) // 2, (screen.get_height() - box_height) // 2, box_width, box_height)

    # Draw white border
    border_thickness = 2
    border_rect = pygame.Rect(game_over_box.left - border_thickness, 
                               game_over_box.top - border_thickness, 
                               game_over_box.width + 2 * border_thickness, 
                               game_over_box.height + 2 * border_thickness)
    pygame.draw.rect(screen, s.WHITE, border_rect)

    # Draw black box
    pygame.draw.rect(screen, s.BLACK, game_over_box)

    # Render and center the "Game Over" text
    game_over_text = s.FONT.render("Game Over", True, s.WHITE)
    game_over_text_rect = game_over_text.get_rect(center=(game_over_box.centerx - 3, game_over_box.top + 25))
    screen.blit(game_over_text, game_over_text_rect)

    # Render Score
    score_text = s.FONT.render("Score: %s" %score, True, s.WHITE)
    score_text_rect = game_over_text.get_rect(center=(game_over_box.centerx, game_over_box.top + 60))
    screen.blit(score_text, score_text_rect)

    # Render buttons
    play_again_button_rect = u.outline_text_w_box(screen, "Play Again", 325, -80)
    main_menu_button_rect = u.outline_text_w_box(screen, "Main Menu", 325, 80)

    pygame.display.flip()

    return play_again_button_rect, main_menu_button_rect