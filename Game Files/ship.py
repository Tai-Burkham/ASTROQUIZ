"""
File: ship.py
Author: Calvin Leavy, Ahmed Krubally, Michelle Orru, Tailor Burkham

Description:
Module for ship and laser classes, handling ship movement, 
ship respawn, new ship, image, collisions, and laser shooting.
"""
import pygame
import math
import settings as s

# Constants for ship movement
ACCELERATION = 0.5
MAX_SPEED = 5

# Constants for ship respawn and invulnerability
RESPAWN_DURATION = 1  # in seconds
INVULNERABILITY_DURATION = 3000  # in miliseconds
BLINK_INTERVAL = 200  # in miliseconds

# Global variables for ship invulnerability and blinking
is_invulnerable = False
is_blinking = False
invulnerability_start_time = 0
blink_last_toggle_time = 0

# Global variable for ship image
ship_image = None
ship_image_file = None

class Ship(pygame.sprite.Sprite):
    """
    Class representing the player's ship.
    """
    def __init__(self):
        super().__init__()
        self.original_image = None

        # Load the ship image
        self.load_ship_image()  

        # Initialize ship variables
        if self.original_image is not None:
            self.original_image = pygame.transform.scale(self.original_image, (75, 75))
            self.image = self.original_image  # Set the initial image
            self.rect = self.image.get_rect()
            self.rect.center = (s.WIDTH // 2, s.HEIGHT // 2)
            self.angle = 0
            self.x_speed = 0
            self.y_speed = 0
            self.acceleration_x = 0
            self.acceleration_y = 0
            self.mask = pygame.mask.from_surface(self.image)
            self.visible = True

    def load_ship_image(self):
        """
        Load the ship image from the settings file.
        """

        global ship_image_file

        # Load ship image setting from file
        with open('settings.txt', 'r') as f:
            for line in f:
                key, value = line.strip().split('=')
                if key == 'ship_image_file':
                    ship_image_file = value.strip()

        # Load the ship image
        if ship_image_file is not None:
            self.original_image = pygame.image.load(ship_image_file)
            self.original_image = pygame.transform.rotate(self.original_image, -90)
    
    def update_ship_image(self):
        """
        Update the ship's image.
        """

        s.ship_updated = False
        self.load_ship_image()

        # Sets ship variables for new image
        if self.original_image is not None:
            self.original_image = pygame.transform.scale(self.original_image, (75, 75))
            self.image = self.original_image
            self.rect = self.image.get_rect()
            self.rect.center = (s.WIDTH // 2, s.HEIGHT // 2)
            self.mask = pygame.mask.from_surface(self.image)

    def update(self, forward, reverse, left_turn, right_turn):
        """
        Update the ship's position and orientation based on user input.
        """

        global is_blinking

        # Update ship image if it is changed in settings
        if s.ship_updated:
            self.update_ship_image()

        # Rotate the ship
        if left_turn:
            self.angle -= 5
            if self.angle < 0:
                self.angle += 360
        if right_turn:
            self.angle += 5
            if self.angle > 360:
                self.angle -= 360

        # Rotate the ship's image based off angle
        self.image = pygame.transform.rotate(self.original_image, -self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)

        # Calculate movement direction based on ship's orientation
        if forward:
            self.acceleration_x = ACCELERATION * math.cos(math.radians(self.angle))
            self.acceleration_y = ACCELERATION * math.sin(math.radians(self.angle))
            self.x_speed += self.acceleration_x
            self.y_speed += self.acceleration_y

            # Limit speed ship speed
            speed = math.sqrt(self.x_speed ** 2 + self.y_speed ** 2)
            if speed > MAX_SPEED:
                ratio = MAX_SPEED / speed
                self.x_speed *= ratio
                self.y_speed *= ratio

        elif reverse:
            # Reduce ship's speed
            self.x_speed *= 0.9
            self.y_speed *= 0.9

        # Update ship's position based on current speed and direction
        self.rect.x += self.x_speed
        self.rect.y += self.y_speed

        # Wrap around screen edges
        if self.rect.left > s.WIDTH - 10:  # Off the right edge
            self.rect.right = 25 
        elif self.rect.right < 10:  # Off the left edge
            self.rect.left = s.WIDTH - 25  
        if self.rect.bottom < 10:  # Off the top edge
            self.rect.top = s.HEIGHT - 25 
        elif self.rect.top > s.HEIGHT - 10:  # Off the bottom edge
            self.rect.bottom = 25

        # Toggle visibility if blinking during respawn
        if is_blinking:
            self.visible = False
        else:
            self.visible = True

    def respawn_ship(ship):
        """
        Respawn the ship in the center of the game map.
        """

        # Centers ship on screen
        ship.rect.centerx = s.WIDTH // 2
        ship.rect.centery = s.HEIGHT // 2

        # Stop player's momentum
        ship.x_speed = 0
        ship.y_speed = 0

    def handle_collisions(self, ship, asteroids):
        """
        Handle collisions between player and asteroids.
        """

        global is_invulnerable, invulnerability_start_time
        
        collisions = []
        
        # Check for collisions during gameplay
        if not is_invulnerable:
            collisions = pygame.sprite.spritecollide(ship, asteroids, False, pygame.sprite.collide_mask)
        
        # If collisions is detected respawn ship
        if collisions:
            if not is_invulnerable:
                Ship.respawn_ship(ship)
                is_invulnerable = True
                invulnerability_start_time = pygame.time.get_ticks()
                # Returning True will reduce the players lives by 1 in game.py
                return True
        return False     

    def update_invulnerability(self):
        """
        Update ship's invulnerability status.
        """
        global is_invulnerable, is_blinking, blink_last_toggle_time
        
        # Set invulnerability after respawn
        if is_invulnerable:
            current_time = pygame.time.get_ticks()
            if current_time - invulnerability_start_time >= INVULNERABILITY_DURATION:
                # Invulnerability duration has passed
                is_invulnerable = False
                is_blinking = False
            elif current_time - blink_last_toggle_time >= BLINK_INTERVAL:
                # Toggle blinking
                is_blinking = not is_blinking
                blink_last_toggle_time = current_time


class Laser(pygame.sprite.Sprite):
    """
    Class representing the laser fired by the ship.
    """
    def __init__(self, start_pos, ship_angle):
        super().__init__()
        self.original_image = pygame.Surface((2, 2))  # Create laser surface
        self.original_image.fill((255, 0, 0))  # Red color for laser
        self.image = pygame.transform.rotate(self.original_image, ship_angle)
        self.rect = self.image.get_rect()
        self.rect.center = start_pos

        # Angle of laser from ships position
        self.angle = ship_angle
        self.speed = 10
        self.lifetime = 60  # Frames the laser is visible

    def update(self):
        """
        Update the laser's position.
        """
        # Moves the laser
        self.rect.x += self.speed * math.cos(math.radians(self.angle))
        self.rect.y += self.speed * math.sin(math.radians(self.angle))

        # Reduce time laser is on screen by 1
        self.lifetime -= 1

    def draw(self, screen):
        """
        Draw the laser on the screen.
        """
        screen.blit(self.image, self.rect)        