import pygame
import time

import settings as s
import game_over_screen
import high_scores
from question import *
from ship import *
from asteroid import Asteroid
from Explosion import *
from high_scores import *
from pygame.locals import *

# Constants
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
# Define constants for player respawn and invulnerability
RESPAWN_DURATION = 1  # in seconds
INVULNERABILITY_DURATION = 3  # in seconds
BLINK_INTERVAL = 0.2  # in seconds

background_image = pygame.image.load("Images and designs/BG.jpg")
background_image = pygame.transform.scale(background_image, (s.WIDTH, s.HEIGHT))

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

# Main game method
def game(screen):
    global game_over, ship_lives, score
    
    # Initialize score variable
    score = 0
 
    # Load highest score
    highest_score = high_scores.load_high_score()
    questions = load_questions("Game Files/data/questions.json", s.question_series) 

    game_over = False
    game_paused = False
    
    # Initialize player lives, adjust as needed for debugging
    ship_lives = 1
    laser_cooldown = 0
    laser_count = 0
    
    asteroids_destroyed = 0
    correct_answer = 0
    generate_asteroids()

    # Initial movement variables
    forward = False
    reverse = False  
    left_turn = False
    right_turn = False

    clock = pygame.time.Clock()

    # Font initialization
    # font = pygame.font.Font(None, 36)  # You can adjust the font size as needed
    
    # Game loop
    while True:
        firing = False
        laser_group = pygame.sprite.Group()
        explosion_group = pygame.sprite.Group()
        
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
                         firing = True
                    if event.key == pygame.K_p:
                        game_paused = not game_paused
                    # Need to impliment:
                    # Mouse and/or keyboard input for questions 
                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_w or event.key == pygame.K_s or event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                        forward = False
                        reverse = False
                    elif event.key == pygame.K_a or event.key == pygame.K_d or event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                        left_turn = False
                        right_turn = False
                    if event.key == pygame.K_SPACE:
                        firing = False
            
            if not game_paused:
                # Movement updates
                # Asteroid Movement
                for asteroid in asteroid_group:
                    if isinstance(asteroid, Asteroid):
                        asteroid.update()

                # Ship Movement 
                ship.update(forward, reverse, left_turn, right_turn) 
                # Laser Movement
                laser_group.update() 

                explosion_group.update()

                # Interactions
                # Laser Shooting
                if firing and laser_cooldown <= 0:
                    # Fire a burst of lasers
                    laser = Laser(ship.rect.center, ship.angle)
                    laser_group.add(laser)
                    laser_count += 1
                    if laser_count >= 10:
                        laser_cooldown = 15 # Adjust this for cooldown time 30 is 1 second
                        laser_count = 0
                # Update the laser cooldown
                if laser_cooldown > 0:
                    laser_cooldown -= 1    

                # Handle collisions with ship and asteroid
                handle_collisions(ship, asteroid_group)
                # Update player's invulnerability status after collision with asteroid
                update_invulnerability()
                
                # If a laser hits an asteroid, create an explosion and remove the asteroid
                for laser in laser_group:    
                    # Check for collisions between the laser and asteroids
                    collisions = pygame.sprite.spritecollide(laser, asteroid_group, True)
                    if collisions:
                        for asteroid in collisions:
                            # Increment asteroids destroyed count
                            asteroids_destroyed += 1
                            
                            # Check for question call
                            if asteroids_destroyed % 2 == 0:
                                
                                correct_answer = display_question(screen, questions)
                                #game_paused = True

                                if correct_answer == True:
                                    score += 1000
                                else:
                                    score -= 1000
                            # Create an explosion at the asteroid's position
                            explosion = Explosion(asteroid.rect.center)
                            explosion_group.add(explosion) 

                            # Increment score
                            score += 100
                            laser.kill()
                            generate_asteroids(1)
                    
                laser_group = pygame.sprite.Group([laser for laser in laser_group if laser.lifetime > 0])

                # Draw everything
                # Add background image
                screen.blit(background_image, (0, 0))

                #drawing all the assest
                asteroid_group.draw(screen)
                laser_group.draw(screen) 
                explosion_group.draw(screen)

                # Draw player only if not invulnerable or blinking
                if not is_invulnerable or (is_invulnerable and is_blinking):
                    ship_group.draw(screen)
                
                # Update the highest score if the current score is higher
                # if score > highest_score:
                # highest_score = score
                # high_scores.save_high_score(highest_score)
                
                #render the cureent score at the top of the screen 
                score_text = font.render(f"Score: {score}", True, (255, 0, 0))
                screen.blit(score_text, (10, 10))  # Position score text at top left corner

                # If our of lives end game
                if ship_lives <= 0:
                    game_over = True

                pygame.display.flip()

                # Render text surfaces for debugging
                # speed_text = font.render(f"Speed: ({ship.x_speed:.2f}, {ship.y_speed:.2f})", True, WHITE)
                # angle_text = font.render(f"Angle: {ship.angle}", True, WHITE)
                # coord_text = font.render(f"Coords: ({ship.rect.centerx}, {ship.rect.centery})", True, WHITE)

                # # Blit text onto the screen
                # screen.blit(speed_text, (10, 10))  # Adjust the position as needed
                # screen.blit(angle_text, (10, 30))
                # screen.blit(coord_text, (10, 50))

                # This controls game speed
                clock.tick(30)

        asteroid_group.empty()

        # Reposition the ship in the middle of the screen
        ship.rect.centerx = s.WIDTH // 2
        ship.rect.centery = s.HEIGHT // 2
        # Put up game over screen and initialize buttons
        play_again_button_rect, main_menu_button_rect = game_over_screen.game_over_screen(screen, score)

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