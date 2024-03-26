import pygame
import utilities as u

# needed for font setting
pygame.init()

# Game Settings
WIDTH, HEIGHT = 900, 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
FONT = pygame.font.Font(None, 36)
FONT_SMALL = pygame.font.Font(None, 24)
TEXT_COLOR = (255, 255, 255)

background_image = pygame.image.load("Game Files/assets/images/menubackground.jpg")
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))

question_series = "ACM Ethics"

def edit_settings(screen) :
    running = True
    while running:
        # Handles events, This is where all mouse and keyboard inputs will be
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        screen.fill(WHITE)
        screen.blit(background_image, (0, 0))

        u.outline_text(screen, "This is where you can edit settings and settings are saved here.", 300, FONT)

        u.outline_text(screen, "Hit X to go back.", 350, FONT)

        pygame.display.flip()


        #difficulty 
        #turn off questions 
        #resize the game page
        #ship choice