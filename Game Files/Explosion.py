import pygame

class Explosion(pygame.sprite.Sprite):
    def __init__(self, center):
        super().__init__()
        self.sprite_sheet = pygame.image.load("Game Files/assets/images/explosionforgame.png").convert_alpha()
        self.rect = self.sprite_sheet.get_rect()
        self.rect.center = center
        self.frame_width = self.rect.width // 8
        self.frame_height = self.rect.height // 8
        self.current_frame = 0
        self.animation_speed = 3  # Adjust as needed
        self.frames = [(i % 8 * self.frame_width, i // 8 * self.frame_height, self.frame_width, self.frame_height) for i in range(64)]
        self.image = self.sprite_sheet.subsurface(self.frames[self.current_frame])

    def update(self):
        self.current_frame += 1
        if self.current_frame >= len(self.frames):
            self.kill()
        else:
            self.image = self.sprite_sheet.subsurface(self.frames[self.current_frame])
