import pygame
import math
from settings import WIDTH, HEIGHT

ACCELERATION = 0.5
MAX_SPEED = 5

ship_image = pygame.image.load("Game Files/assets/images/Spaceship_1.png")
ship_image = pygame.transform.rotate(ship_image, -90)
missile_image = pygame.image.load("Game Files/assets/images/missle.jpg")
class Ship(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.original_image = pygame.transform.scale(ship_image, (75, 75))
        self.image = self.original_image  # Set the initial image
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH // 2, HEIGHT // 2)
        self.angle = 0
        self.x_speed = 0
        self.y_speed = 0
        self.acceleration_x = 0
        self.acceleration_y = 0
        self.mask = pygame.mask.from_surface(self.image)
        self.missile_group = pygame.sprite.Group()  # Group to store missiles
        
    def update(self, forward, reverse, left_turn, right_turn):
        # Rotate the ship
        if left_turn:
            self.angle -= 2
            if self.angle < 0:
                self.angle += 360
        if right_turn:
            self.angle += 2
            if self.angle > 360:
                self.angle -= 360
        
        
        # Rotate the ship's image
        self.image = pygame.transform.rotate(self.original_image, -self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)  # Adjust the rect after rotation
        space_pressed = False
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
        if self.rect.left > WIDTH - 10:  # Ship has moved off the right edge
            self.rect.right = 25  # Move ship to the left edge
        elif self.rect.right < 10:  # Ship has moved off the left edge
            self.rect.left = WIDTH - 25  # Move ship to the right edge
        if self.rect.bottom < 10:  # Ship has moved off the top edge
            self.rect.top = HEIGHT - 25  # Move ship to the bottom edge
        elif self.rect.top > HEIGHT - 10:  # Ship has moved off the bottom edge
            self.rect.bottom = 25  # Move ship to the top edge

      

    def shoot_missile(self):
        # Create a new missile
        missile = Missile(self.rect.center, self.angle)
        # Add missile to the missile group
        self.missile_group.add(missile)

    def shoot(self):
        # Create a new Missile object and add it to the sprite group
        missile = Missile (self.rect.center, self.angle)
        self.missile_group.add(missile)

    def respawn_ship(ship):
        """Respawn the ship in the center of the game map."""
        ship.rect.centerx = WIDTH // 2
        ship.rect.centery = HEIGHT // 2
        # Stop player's momentum
        ship.x_speed = 0
        ship.y_speed = 0
class Missile(pygame.sprite.Sprite):
    def __init__(self, position, angle):
        super().__init__()
        # Set missile image and initial position
        self.image = pygame.transform.rotate(missile_image, -angle)
        self.rect = self.image.get_rect(center=position)
        self.angle = angle
        self.speed = 10  # Missile speed

    def update(self):
        # Move missile in the direction of its angle
        self.rect.x += self.speed * math.cos(math.radians(self.angle))
        self.rect.y -= self.speed * math.sin(math.radians(self.angle))  # Negative sign to account for flipped y-axis

        # Remove missile when it goes off-screen
        if self.rect.left > WIDTH or self.rect.right < 0 or self.rect.top > HEIGHT or self.rect.bottom < 0:
            self.kill()  # Remove the missile from all sprite groups


  

   

    def shoot(self):
        # Create a new Missile object and add it to the sprite group
        missile = Missile(self.rect.centerx, self.rect.centery, self.angle)
        self.missile_group.add(missile)
'''
class Missile(pygame.sprite.Sprite):
    def __init__(self, x, y, angle):
        super().__init__()
        self.image = pygame.Surface((5, 5))  # Adjust size as needed
        self.image.fill((255, 0, 0))  # Red color for the missile
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.angle = angle
        self.speed = 10  # Adjust speed as needed
        self.dx = self.speed * math.cos(math.radians(self.angle))
        self.dy = self.speed * math.sin(math.radians(self.angle))

    def update(self):
        self.rect.x += self.dx
        self.rect.y += self.dy
        '''