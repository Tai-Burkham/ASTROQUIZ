"""
File: game.py
Author: Calvin Leavy, Ahmed Krubally, Michelle Orru, Tailor Burkham

Description:
This file is where the game is controlled from. It handles all screen activity
as well as all user input during gameplay. This file takes in data from settings.py,
ship.py, asteroid.py, explosion.py, and high_scores.py. After game is over it calls
game_over_screen.py and handles its inputs.

"""

import pygame
import sys
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

# Load background image
background_image = pygame.image.load("assets/images/BG.jpg")
background_image = pygame.transform.scale(background_image, (s.WIDTH, s.HEIGHT))

# Load health Icon image
health_image = pygame.image.load("assets/images/health_heart.png")
health_image = pygame.transform.scale(health_image, (40, 40))

# Initializes ship sprite
ship = Ship()
ship_group = pygame.sprite.Group()
ship_group.add(ship)

# Load Sound
sound_Explosion = pygame.mixer.Sound("assets/audio/soundEffects/explosion-91872.mp3")

# Generates asteroids
asteroid_group = pygame.sprite.Group()
def generate_asteroids(num_asteroids = 10):
    """
    Generates asteroid sprites

    Args:
        num_asteroids(int): Number of asteroids to be generated

    Returns:
        None
    """
    for _ in range(num_asteroids):
        asteroid = Asteroid()
        asteroid_group.add(asteroid)

# Main game method
def game(screen):
    """
    The main game loop.

    Args:
        screen: The Pygame display surface.

    Returns:
        None
    """
    global game_over, ship_lives, score
    
    # Initialize score variable
    score = 0
    score_multiplier = 1
 
    # Load highest score
    highest_score = high_scores.load_high_score()
    questions = load_questions("data/questions.json", s.question_series) 

    game_over = False
    game_paused = False
    
    # Initialize player lives
    ship_lives = 1

    # Initialize laser settings
    laser_cooldown = 0
    laser_count = 0
    
    # Initialize score settings
    asteroids_destroyed = 0
    correct_answer = False
    num_correct = 0
    num_questions = 0
    result_timer = 0

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
        explosion_group = pygame.sprite.Group()
        
        while not game_over:
            # Handles events
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

                # Updates explosions for destroyed asteroids
                explosion_group.update()

                # Interactions
                # Laser Shooting
                if firing and laser_cooldown <= 0:
                    # Fire a burst of lasers
                    laser = Laser(ship.rect.center, ship.angle)
                    laser_group.add(laser)

                    # Reduce score for every laser shot
                    score -= 1
                    laser_count += 1
                    
                    # After 10 shots fired begin weapon cooldown
                    if laser_count >= 10:
                        laser_cooldown = 15 
                        laser_count = 0

                # Update the laser cooldown
                if laser_cooldown > 0:
                    laser_cooldown -= 1    

                # Handle collisions with ship and asteroid and reduce lives
                collision_occured = ship.handle_collisions(ship, asteroid_group)
                if collision_occured:
                    sound_Explosion.play()
                    ship_lives -= 1
                
                # Handle ship invulnerability cooldown
                ship.update_invulnerability()
                
                # If a laser hits an asteroid, create an explosion and remove the asteroid
                for laser in laser_group:    
                    # Check for collisions between the laser and asteroids
                    collisions = pygame.sprite.spritecollide(laser, asteroid_group, True)
                    if collisions:
                        for asteroid in collisions:
                            # Increment asteroids destroyed count
                            asteroids_destroyed += 1
                            
                            # Call questions based off amount of asteroids destroyed
                            if asteroids_destroyed % 7 == 0: # change frequency of questions
                                num_questions += 1
                                correct_answer = display_question(screen, questions)

                                # If correct answer increase score, score multiplier, and if health is low add one
                                if correct_answer == True:
                                    score += 1000
                                    score_multiplier += 1
                                    num_correct += 1
                                    if ship_lives < 3:
                                        ship_lives += 1
                                # If wrong answer
                                else:
                                    score -= 1000
                                    score_multiplier = 1
                                
                                # Timer for rendering question results on top of screen
                                result_timer = 60

                            # Create an explosion at the asteroid's position
                            explosion = Explosion(asteroid.rect.center)
                            explosion_group.add(explosion) 

                            # Increment score and remove laser
                            score += (100 * score_multiplier)
                            laser.kill()

                            # Replace destroyed asteroid
                            generate_asteroids(1)
                    
                laser_group = pygame.sprite.Group([laser for laser in laser_group if laser.lifetime > 0])

                # Draw everything
                # Add background image
                screen.blit(background_image, (0, 0))

                # Drawing all the assets
                asteroid_group.draw(screen)
                laser_group.draw(screen) 
                explosion_group.draw(screen)

                # Draw player only if not invulnerable or blinking
                if ship.visible:
                    ship_group.draw(screen)
                
                # Update the highest score if the current score is higher
                if score > highest_score:
                    highest_score = score
                    high_scores.save_high_score(highest_score)
                
                # Render question result on top center of screen
                if result_timer > 0:
                    result_timer -= 1
                    if correct_answer == True:
                        result_text = font.render("Correct!", True, (255, 255, 255))
                    else:
                        result_text = font.render("Incorrect", True, (255, 0, 0))
                    screen.blit(result_text, ((s.WIDTH // 2) - 30, 10))

                # Render the cureent score
                score_text = font.render(f"Score: {score} x {score_multiplier}", True, (255, 0, 0))
                screen.blit(score_text, (10, 10))  

                # Render health hearts
                x_offset = 0
                for i in range(ship_lives):
                    screen.blit(health_image, (10 + x_offset, 30))
                    x_offset += 40

                # If out of lives end game
                if ship_lives <= 0:
                    game_over = True

                pygame.display.flip()

                # This controls game speed
                clock.tick(30)

        asteroid_group.empty()

        # Reposition the ship in the middle of the screen
        ship.rect.centerx = s.WIDTH // 2
        ship.rect.centery = s.HEIGHT // 2

        # Put up game over screen and initialize buttons
        play_again_button_rect, main_menu_button_rect = game_over_screen.game_over_screen(screen, score, num_correct, num_questions)

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
