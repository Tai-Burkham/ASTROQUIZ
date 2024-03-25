import pygame
import settings as s
import utilities as u
# from settings import WIDTH, HEIGHT, WHITE, BLACK, FONT


background_image = pygame.image.load("Game Files/assets/images/menubackground.jpg")
background_image = pygame.transform.scale(background_image, (s.WIDTH, s.HEIGHT))

def edit_questions(screen) :
    running = True
    while running:
        # Handles events, This is where all mouse and keyboard inputs will be
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        screen.fill(s.WHITE)
        screen.blit(background_image, (0, 0))

        u.outline_text(screen, "This is where you can edit questions. Hit X to go back.", 300, s.FONT)
        # text = FONT.render("This is where you can edit questions. Hit X to go back.", True, (255, 255, 255))
        # screen.blit(text, (WIDTH // 2 - text.get_width() // 2 - 1, 300))

        pygame.display.flip()