import pygame
import settings as s
#from settings import WIDTH, HEIGHT, WHITE, BLACK, FONT

background_image = pygame.image.load("Game Files/assets/images/menubackground.jpg")
background_image = pygame.transform.scale(background_image, (s.WIDTH, s.HEIGHT))

def view_High_Scores(screen) :
    running = True
    while running:
        # Handles events, This is where all mouse and keyboard inputs will be
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        screen.fill(s.WHITE)
        screen.blit(background_image, (0, 0))

        s.outline_text(screen, "This is where you can view the High Scores. Hit X to go back.", 300)

        pygame.display.flip()