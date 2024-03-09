import pygame
from ship import Ship
from asteroid import Asteroid
from pygame.locals import *
from settings import WIDTH, HEIGHT

# Constants
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

ship = Ship()
ship_group = pygame.sprite.Group()
ship_group.add(ship)

asteroid_group = pygame.sprite.Group()
# generate asteroids
num_asteroids = 10
for _ in range(num_asteroids):
    asteroid = Asteroid()
    asteroid_group.add(asteroid)

# Main game method
def game(screen):
    game_over = False
    global x_speed, y_speed, x_coord, y_coord, angle

    # Initial movement variables
    forward = False
    reverse = False  
    left_turn = False
    right_turn = False
    
    font = pygame.font.SysFont(None, 24)

    clock = pygame.time.Clock()
    
    # Game loop
    while not game_over:
        # Handles events, This is where all mouse and keyboard inputs will be
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    game_over = True
                if event.key == pygame.K_w or event.key == pygame.K_UP:
                    forward = True
                if event.key == pygame.K_s or event.key == pygame.K_DOWN:
                    reverse = True
                if event.key == pygame.K_a or event.key == pygame.K_LEFT:
                    left_turn = True
                if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                    right_turn = True
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
        
        # astroid movement goes here
        for asteroid in asteroid_group:
            if isinstance(asteroid, Asteroid):
                asteroid.update()

        # Ship Movement 
        ship.update(forward, reverse, left_turn, right_turn) 

        # Update game logic
        # interactions with astroids between ship
        collisions = pygame.sprite.spritecollide(ship, asteroid_group, False, pygame.sprite.collide_mask)
        if collisions:
            print("Collision detected!")

        # Draw everything
        screen.fill(BLACK)

        asteroid_group.draw(screen)
        ship_group.draw(screen)
        
        # Render text surfaces for debugging
        speed_text = font.render(f"Speed: ({ship.x_speed:.2f}, {ship.y_speed:.2f})", True, WHITE)
        angle_text = font.render(f"Angle: {ship.angle}", True, WHITE)
        coord_text = font.render(f"Coords: ({ship.rect.centerx}, {ship.rect.centery})", True, WHITE)

        # Blit text onto the screen
        screen.blit(speed_text, (10, 10))  # Adjust the position as needed
        screen.blit(angle_text, (10, 30))
        screen.blit(coord_text, (10, 50))

        pygame.display.flip()

        # This controls game speed
        clock.tick(30)