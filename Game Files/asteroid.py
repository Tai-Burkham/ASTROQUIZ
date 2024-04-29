"""
File: asteroid.py
Author: Calvin Leavy, Ahmed Krubally, Michelle Orro, Tailor Burkham

Description:
This file handles the class for asteroid including its movement and
generation.

"""
import pygame
import math
import random
from settings import WIDTH, HEIGHT

asteroid_image = pygame.image.load("assets/images/Asteroid_3.png")

class Asteroid(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # Randomly choose the radius within the desired range
        self.radius = random.randint(15, 30)
        self.image = asteroid_image
        # Scale the image based on the radius
        self.image = pygame.transform.scale(self.image, (2 * self.radius, 2 * self.radius))
        self.rect = self.image.get_rect()
        self.spawn_offscreen()  # Spawn off-screen initially

        self.speed = random.randint(1, 5)
        self.angle = math.radians(random.randint(0, 360))
        # Create mask for asteroid
        self.mask = pygame.mask.from_surface(self.image)

    def spawn_offscreen(self):
        side = random.choice(["top", "bottom", "left", "right"])
        if side == "top":
            self.rect.x = random.randint(0, WIDTH - self.rect.width)
            self.rect.y = -self.rect.height
        elif side == "bottom":
            self.rect.x = random.randint(0, WIDTH - self.rect.width)
            self.rect.y = HEIGHT
        elif side == "left":
            self.rect.x = -self.rect.width
            self.rect.y = random.randint(0, HEIGHT - self.rect.height)
        elif side == "right":
            self.rect.x = WIDTH
            self.rect.y = random.randint(0, HEIGHT - self.rect.height)

    def update(self):
        # Update asteroid position
        self.rect.x += self.speed * math.cos(self.angle)
        self.rect.y += self.speed * math.sin(self.angle)
        # Check if asteroid is completely off-screen, if so, respawn it
        if self.rect.right < 0 or self.rect.left > WIDTH or self.rect.bottom < 0 or self.rect.top > HEIGHT:
            self.spawn_offscreen()
            self.angle = math.radians(random.randint(0, 360))
            # Randomize the size of the asteroid
            self.radius = random.randint(15, 30)  # Or choose your desired range for the size
            self.image = pygame.transform.scale(self.image, (2 * self.radius, 2 * self.radius))
            self.mask = pygame.mask.from_surface(self.image)

