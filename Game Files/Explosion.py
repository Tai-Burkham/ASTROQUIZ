import pygame

class Explosion(pygame.sprite.Sprite):
    def __init__(self, position, duration=1):
        super().__init__()
        self.images = []  # List to hold the explosion animation frames
        self.index = 0    # Current index of the image being displayed
        self.load_images()  # Load the explosion animation frames
        self.image = self.images[self.index]  # Set the initial image
        self.rect = self.image.get_rect(center=position)  # Set the position of the explosion
        self.duration = duration  # Duration of the explosion in seconds
        self.start_time = pygame.time.get_ticks()  # Record the start time of the explosion

    def load_images(self):
        for i in range(6):  # Assuming there are 6 frames in your explosion animation
            img = pygame.image.load(f"Game Files/assets/images/explosion{i}.png")  # Load each frame
            img = pygame.transform.scale(img, (100, 100))  # Scale the image if needed
            self.images.append(img)  # Append the image to the list of frames

    def update(self):
        now = pygame.time.get_ticks()  # Get the current time
        elapsed = (now - self.start_time) / 1000  # Convert milliseconds to seconds

        # Calculate the index of the image based on elapsed time and duration
        self.index = int(elapsed / self.duration * len(self.images))
        if self.index >= len(self.images):
            self.kill()  # Kill the explosion sprite when the animation ends
        else:
            self.image = self.images[self.index]  # Update the image to the current frame
