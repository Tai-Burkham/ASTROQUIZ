import pygame
import math
from main import WIDTH, HEIGHT

# Constants
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GRAY = (105, 106, 107)

ACCELERATION = 0.5
MAX_SPEED = 5

ship_image = pygame.image.load("Game Files/assets/images/Spaceship_1.png")
ship_image = pygame.transform.scale(ship_image, (100, 100))
ship_image.set_colorkey(BLACK)

# Draws the ship on the screen at given location and angle
def draw_ship(screen, x, y, angle):
    rotated_ship = pygame.transform.rotate(ship_image, angle - 90)
    ship_rect = rotated_ship.get_rect(center=(x, y))
    screen.blit(rotated_ship, ship_rect)


def game(screen):
    game_over = False
    global score, health

    # Variables
    # Ship movement
    forward = False
    reverse = False
    x_speed = 0
    y_speed = 0
    acceleration_x = 0
    acceleration_y = 0
    left_turn = False
    right_turn = False
    angle = 90
    # Ship starting location
    x_coord = WIDTH // 2
    y_coord = HEIGHT // 2

    font = pygame.font.SysFont(None, 24)

    clock = pygame.time.Clock()
    
    # Game loop
    while not game_over:
        # Handle events, This is where all mouse and keyboard inputs will be
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    game_over = True
                if event.key == pygame.K_w:
                    forward = True
                if event.key == pygame.K_s:
                    reverse = True
                if event.key == pygame.K_a:
                    left_turn = True
                if event.key == pygame.K_d:
                    right_turn = True

            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_w or event.key == pygame.K_s:
                    forward = False
                    reverse = False
                elif event.key == pygame.K_a or event.key == pygame.K_d:
                    left_turn = False
                    right_turn = False
        
        # Ship Movement         
        # Turning
        if left_turn:
            angle -= 2
            if angle < 0:
                angle = 360
        if right_turn:
            angle += 2
            if angle > 360:
                angle = 0

        # Acceleration / Deceleration
        if forward:
            # controls acceleration based on direction ship is pointing when giving it the gas
            acceleration_x = ACCELERATION * math.cos(math.radians(angle))
            acceleration_y = ACCELERATION * -math.sin(math.radians(angle))
            x_speed += acceleration_x
            y_speed += acceleration_y

            # Puts a speed limit in for the ship
            speed = math.sqrt(x_speed ** 2 + y_speed ** 2)
            if speed > MAX_SPEED:
                ratio = MAX_SPEED / speed
                x_speed *= ratio
                y_speed *= ratio
        elif reverse:
            # For simplicity, reversing will simply reduce the ship's speed, We can change it to actually reverse if we think we need it later
            x_speed *= 0.9
            y_speed *= 0.9
               
        x_coord += x_speed
        y_coord += y_speed

        x_coord %= WIDTH
        y_coord %= HEIGHT
 
        # astroid generation and movement goes here


        screen.fill(BLACK)

        # Update game logic
        # interactions with astroids between ship

        

        # Draw everything

        draw_ship(screen, x_coord, y_coord, angle)
        
        # Render text surfaces
        speed_text = font.render(f"Speed: ({x_speed:.2f}, {y_speed:.2f})", True, WHITE)
        angle_text = font.render(f"Angle: {angle}", True, WHITE)
        coord_text = font.render(f"Coords: ({x_coord}, {y_coord})", True, WHITE)

        # Blit text onto the screen
        screen.blit(speed_text, (10, 10))  # Adjust the position as needed
        screen.blit(angle_text, (10, 30))
        screen.blit(coord_text, (10, 50))

        pygame.display.flip()

        # This controls game speed
        clock.tick(30)