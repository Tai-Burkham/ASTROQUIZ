import pygame
from ship import Ship
from asteroid import Asteroid
from pygame.locals import *
from settings import WIDTH, HEIGHT
import time


# Constants
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

background_image = pygame.image.load("Images and designs/BG.jpg")
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))

ship = Ship()
ship_group = pygame.sprite.Group()
ship_group.add(ship)

asteroid_group = pygame.sprite.Group()
# generate asteroids
num_asteroids = 10
for _ in range(num_asteroids):
    asteroid = Asteroid()
    asteroid_group.add(asteroid)

# Define constants for player respawn and invulnerability
RESPAWN_DURATION = 1  # in seconds
INVULNERABILITY_DURATION = 3  # in seconds
BLINK_INTERVAL = 0.2  # in seconds

# Global variables to track player's invulnerability and blinking
is_invulnerable = False
is_blinking = False
invulnerability_start_time = 0
blink_last_toggle_time = 0


def respawn_ship(ship):
    """Respawn the ship in the center of the game map."""
    ship.rect.centerx = WIDTH // 2
    ship.rect.centery = HEIGHT // 2
     # Stop player's momentum
    ship.x_speed = 0
    ship.y_speed = 0

def handle_collisions(ship, asteroid):
    """Handle collisions between the ship and asteroids."""
    global is_invulnerable, invulnerability_start_time
    
    collisions = []
    if not is_invulnerable:
        collisions = pygame.sprite.spritecollide(ship, asteroid, False, pygame.sprite.collide_mask)
    
    if collisions:
        print("Collision detected!")
        if not is_invulnerable:
            respawn_ship(ship)
            is_invulnerable = True
            invulnerability_start_time = time.time()
            is_blinking = True
            blink_last_toggle_time = time.time()

def update_invulnerability():
    """Update player's invulnerability status."""
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

         # Handle collisions
        handle_collisions(ship, asteroid_group)


         # Update player's invulnerability status
        update_invulnerability()
        
        

        #OLD LOGIC I WANT TO KEEP JUST IN CASE
        # Update game logic
        # interactions with astroids between ship
       # collisions = pygame.sprite.spritecollide(ship, asteroid_group, False, pygame.sprite.collide_mask)
        #if collisions:
         #   print("Collision detected!")

         

         

        # Draw everything
       # Fill the screen with a color or image
        screen.blit(background_image, (0, 0))


        asteroid_group.draw(screen)
        #ship_group.draw(screen)
        
         # Draw player only if not invulnerable or blinking
        if not is_invulnerable or (is_invulnerable and is_blinking):
            ship_group.draw(screen)
        
        pygame.display.flip()

        # Render text surfaces for debugging
        speed_text = font.render(f"Speed: ({ship.x_speed:.2f}, {ship.y_speed:.2f})", True, WHITE)
        angle_text = font.render(f"Angle: {ship.angle}", True, WHITE)
        coord_text = font.render(f"Coords: ({ship.rect.centerx}, {ship.rect.centery})", True, WHITE)

        # Blit text onto the screen
        screen.blit(speed_text, (10, 10))  # Adjust the position as needed
        screen.blit(angle_text, (10, 30))
        screen.blit(coord_text, (10, 50))

        #pygame.display.flip()

        # This controls game speed
        clock.tick(30)