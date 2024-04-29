import pygame
import math
import settings as s

ACCELERATION = 0.5
MAX_SPEED = 5

RESPAWN_DURATION = 1  # in seconds
INVULNERABILITY_DURATION = 3000  # in miliseconds
BLINK_INTERVAL = 200  # in miliseconds

is_invulnerable = False
is_blinking = False
invulnerability_start_time = 0
blink_last_toggle_time = 0

# ship_image = pygame.image.load(s.ship_image_file)
# ship_image = pygame.transform.rotate(ship_image, -90)

# Initialize default value
ship_image = None
ship_image_file = None

class Ship(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.original_image = None  # Initially set to None
        self.load_ship_image()  # Load the ship image
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
            self.visible = True  # Add visible attribute

    def load_ship_image(self):
        global ship_image_file
        # Read the settings file
        with open('settings.txt', 'r') as f:
            for line in f:
                key, value = line.strip().split('=')
                if key == 'ship_image_file':
                    ship_image_file = value.strip()
        print("Ship image file:", ship_image_file)  # Add this line to print the loaded ship image file
        # Load the ship image
        if ship_image_file is not None:
            self.original_image = pygame.image.load(ship_image_file)
            self.original_image = pygame.transform.rotate(self.original_image, -90)
    
    def update_ship_image(self):
        s.ship_updated = False
        self.load_ship_image()
        if self.original_image is not None:
            self.original_image = pygame.transform.scale(self.original_image, (75, 75))
            self.image = self.original_image  # Set the image
            self.rect = self.image.get_rect()
            self.rect.center = (s.WIDTH // 2, s.HEIGHT // 2)
            self.mask = pygame.mask.from_surface(self.image)

    def update(self, forward, reverse, left_turn, right_turn):
        global is_blinking
        if s.ship_updated:
            self.update_ship_image()
        # Rotate the ship, adjust self.angle for turning speed
        if left_turn:
            self.angle -= 5
            if self.angle < 0:
                self.angle += 360
        if right_turn:
            self.angle += 5
            if self.angle > 360:
                self.angle -= 360

        # Rotate the ship's image
        self.image = pygame.transform.rotate(self.original_image, -self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)  # Adjust the rect after rotation

        # Calculate movement direction based on ship's orientation
        if forward:
            # Calculate acceleration components based on ship's orientation
            self.acceleration_x = ACCELERATION * math.cos(math.radians(self.angle))
            self.acceleration_y = ACCELERATION * math.sin(math.radians(self.angle))
            self.x_speed += self.acceleration_x
            self.y_speed += self.acceleration_y

            # Limit speed
            speed = math.sqrt(self.x_speed ** 2 + self.y_speed ** 2)
            if speed > MAX_SPEED:
                ratio = MAX_SPEED / speed
                self.x_speed *= ratio
                self.y_speed *= ratio

        elif reverse:
            # For simplicity, reversing will simply reduce the ship's speed, We can change it to actually reverse if needed
            self.x_speed *= 0.9
            self.y_speed *= 0.9

        # Update ship's position
        self.rect.x += self.x_speed
        self.rect.y += self.y_speed

        # Wrap around screen edges, This will need some adjustment
        if self.rect.left > s.WIDTH - 10:  # Ship has moved off the right edge
            self.rect.right = 25  # Move ship to the left edge
        elif self.rect.right < 10:  # Ship has moved off the left edge
            self.rect.left = s.WIDTH - 25  # Move ship to the right edge
        if self.rect.bottom < 10:  # Ship has moved off the top edge
            self.rect.top = s.HEIGHT - 25  # Move ship to the bottom edge
        elif self.rect.top > s.HEIGHT - 10:  # Ship has moved off the bottom edge
            self.rect.bottom = 25  # Move ship to the top edge

        # Toggle visibility if blinking
        if is_blinking:
            self.visible = False
        else:
            self.visible = True

    # def change_ship(self):
    #     global ship_image, ship_image_file
    #     # Read the settings file
    #     with open('settings.txt', 'r') as f:
    #         for line in f:
    #             key, value = line.strip().split('=')
    #             if key == 'ship_image_file':
    #                 ship_image_file = value.strip()
    #     # Load the ship image
    #     if ship_image_file is not None:
    #         new_ship_image = pygame.image.load(ship_image_file)
    #         new_ship_image = pygame.transform.rotate(new_ship_image, -90)
    #         # Update original_image to the new ship image
    #         self.original_image = pygame.transform.scale(new_ship_image, (75, 75))
    #         # Update the mask
    #         self.mask = pygame.mask.from_surface(self.original_image)

    def respawn_ship(ship):
        """Respawn the ship in the center of the game map."""
        ship.rect.centerx = s.WIDTH // 2
        ship.rect.centery = s.HEIGHT // 2
        # Stop player's momentum
        ship.x_speed = 0
        ship.y_speed = 0

    # Handles collisions between player and asteroids.
    def handle_collisions(self, ship, asteroids):
        global is_invulnerable, invulnerability_start_time
        
        collisions = []
        if not is_invulnerable:
            collisions = pygame.sprite.spritecollide(ship, asteroids, False, pygame.sprite.collide_mask)
        
        if collisions:
            if not is_invulnerable:
                Ship.respawn_ship(ship)
                is_invulnerable = True
                invulnerability_start_time = pygame.time.get_ticks()
                # Reduce player's lives by 1
                return True
        return False     

    # Handles ship invulnerability
    def update_invulnerability(self):
        global is_invulnerable, is_blinking, blink_last_toggle_time
        
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
    def __init__(self, start_pos, ship_angle):
        super().__init__()
        self.original_image = pygame.Surface((2, 2))  # Create a rectangular surface
        self.original_image.fill((255, 0, 0))  # Red color for laser
        self.image = pygame.transform.rotate(self.original_image, ship_angle)  # Rotate the image
        self.rect = self.image.get_rect()
        self.rect.center = start_pos

        self.angle = ship_angle
        self.speed = 10
        self.lifetime = 60  # Frames the laser is visible

    def update(self):
        # Move the laser in the direction of its angle
        self.rect.x += self.speed * math.cos(math.radians(self.angle))
        self.rect.y += self.speed * math.sin(math.radians(self.angle))
        self.lifetime -= 1

    def draw(self, screen):
        screen.blit(self.image, self.rect)        