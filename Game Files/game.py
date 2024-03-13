import pygame
from ship import Ship
from ship import Laser
from asteroid import Asteroid
from pygame.locals import *
from settings import WIDTH, HEIGHT, FONT
import time
import settings as s


# Constants
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
# Define constants for player respawn and invulnerability
RESPAWN_DURATION = 1  # in seconds
INVULNERABILITY_DURATION = 3  # in seconds
BLINK_INTERVAL = 0.2  # in seconds

background_image = pygame.image.load("Images and designs/BG.jpg")
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))

ship = Ship()
ship_group = pygame.sprite.Group()
ship_group.add(ship)


# generate asteroids
asteroid_group = pygame.sprite.Group()
def generate_asteroids(num_asteroids = 10):
    for _ in range(num_asteroids):
        asteroid = Asteroid()
        asteroid_group.add(asteroid)

# Global variables to track player's invulnerability and respawn blinking
is_invulnerable = False
is_blinking = False
invulnerability_start_time = 0
blink_last_toggle_time = 0

# Handles collisions between player and asteroids.
def handle_collisions(player, asteroids):
    global is_invulnerable, invulnerability_start_time, ship_lives, game_over
    
    collisions = []
    if not is_invulnerable:
        collisions = pygame.sprite.spritecollide(player, asteroids, False, pygame.sprite.collide_mask)
    
    if collisions:
        print("Collision detected! Lives:%s" %ship_lives)
        if not is_invulnerable:
            Ship.respawn_ship(ship)
            is_invulnerable = True
            invulnerability_start_time = time.time()
            # Reduce player's lives by 1
            ship_lives -= 1      

# Handles ship invulnerability
def update_invulnerability():
    global is_invulnerable, is_blinking, blink_last_toggle_time
    
    if is_invulnerable:
        current_time = time.time()
        if current_time - invulnerability_start_time >= INVULNERABILITY_DURATION:
            # Invulnerability duration has passed
            is_invulnerable = False
            is_blinking = False
        elif current_time - blink_last_toggle_time >= BLINK_INTERVAL:
            # Toggle blinking
            is_blinking = not is_blinking
            blink_last_toggle_time = current_time

def game_over_screen(screen):
    # Clear the asteroid group
    asteroid_group.empty()

    # Reposition the ship in the middle of the screen
    ship.rect.centerx = WIDTH // 2
    ship.rect.centery = HEIGHT // 2

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
    pygame.draw.rect(screen, WHITE, border_rect)

    # Draw black box
    pygame.draw.rect(screen, BLACK, game_over_box)

    # Render and center the "Game Over" text
    game_over_text = FONT.render("Game Over", True, WHITE)
    game_over_text_rect = game_over_text.get_rect(center=(game_over_box.centerx - 3, game_over_box.top + 25))
    screen.blit(game_over_text, game_over_text_rect)

    # Temp score
    score = 100

    # Render Score
    score_text = FONT.render("Score: %s" %score, True, WHITE)
    score_text_rect = game_over_text.get_rect(center=(game_over_box.centerx, game_over_box.top + 60))
    screen.blit(score_text, score_text_rect)

    # Render buttons
    play_again_button_rect = s.outline_text_w_box(screen, "Play Again", 325, -80)
    main_menu_button_rect = s.outline_text_w_box(screen, "Main Menu", 325, 80)

    pygame.display.flip()

    return play_again_button_rect, main_menu_button_rect

# Main game method
def game(screen):
    global game_over, ship_lives

    game_over = False
    
    # Initialize player lives, adjust as needed for debugging
    ship_lives = 1
    generate_asteroids()

    # Initial movement variables
    forward = False
    reverse = False  
    left_turn = False
    right_turn = False

    clock = pygame.time.Clock()
    
    # Game loop
    while True:
        firing = False
        laser_group = pygame.sprite.Group()
        while not game_over:
            # Handles events, This is where all mouse and keyboard inputs will be
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return
                    if event.key == pygame.K_w or event.key == pygame.K_UP:
                        forward = True
                    if event.key == pygame.K_s or event.key == pygame.K_DOWN:
                        reverse = True
                    if event.key == pygame.K_a or event.key == pygame.K_LEFT:
                        left_turn = True
                    if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                        right_turn = True
                    if event.key == pygame.K_SPACE:
                         firing = True     # Fire laser when spacebar is pressed
                    # Need to impliment:
                    # shooting
                    # Mouse and/or keyboard input for questions
                    # Pause

                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_w or event.key == pygame.K_s or event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                        forward = False
                        reverse = False
                    elif event.key == pygame.K_a or event.key == pygame.K_d or event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                        left_turn = False
                        right_turn = False
                    if event.key == pygame.K_SPACE:
                        firing = False
            # astroid movement goes here
            for asteroid in asteroid_group:
                if isinstance(asteroid, Asteroid):
                    asteroid.update()

            # Ship Movement 
            ship.update(forward, reverse, left_turn, right_turn) 
             
            #shoot the lazer
            laser_group.update()

            if firing:
             laser = Laser(ship.rect.center, ship.angle)
             laser_group.add(laser)
                # Handle collisions
            handle_collisions(ship, asteroid_group)


                # Update player's invulnerability status
            update_invulnerability()

            # Draw everything
            # Fill the screen with a color or image
            screen.blit(background_image, (0, 0))


            asteroid_group.draw(screen)
            laser_group.draw(screen) 

            # Draw player only if not invulnerable or blinking
            if not is_invulnerable or (is_invulnerable and is_blinking):
                ship_group.draw(screen)

            pygame.display.flip()

            # Render text surfaces for debugging
            # speed_text = font.render(f"Speed: ({ship.x_speed:.2f}, {ship.y_speed:.2f})", True, WHITE)
            # angle_text = font.render(f"Angle: {ship.angle}", True, WHITE)
            # coord_text = font.render(f"Coords: ({ship.rect.centerx}, {ship.rect.centery})", True, WHITE)



            # # Blit text onto the screen
            # screen.blit(speed_text, (10, 10))  # Adjust the position as needed
            # screen.blit(angle_text, (10, 30))
            # screen.blit(coord_text, (10, 50))

            # If our of lives end game
            if ship_lives <= 0:
                game_over = True

            # This controls game speed
            clock.tick(30)

        # Put up game over screen and initialize buttons
        play_again_button_rect, main_menu_button_rect = game_over_screen(screen)

        # Event handling for game over screen
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return  # Exit the function if the user closes the window
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return  # Exit the function if the user presses ESC
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if play_again_button_rect.collidepoint(event.pos):
                        game(screen)
                        return
                    elif main_menu_button_rect.collidepoint(event.pos):
                        return