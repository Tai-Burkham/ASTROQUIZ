import pygame

pygame.init()

WIDTH, HEIGHT = 900, 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
FONT = pygame.font.Font(None, 36)
TEXT_COLOR = (255, 255, 255)
OUTLINE_COLOR = (0, 0, 0)

background_image = pygame.image.load("Game Files/assets/images/menubackground.jpg")
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))

# Outlines text without box
def outline_text(screen, text, height) :
    text_outline = FONT.render(text, True, OUTLINE_COLOR)
    rendered_text = FONT.render(text, True, WHITE)

    screen.blit(text_outline, (WIDTH // 2 - text_outline.get_width() // 2 - 1, height))
    screen.blit(text_outline, (WIDTH // 2 - text_outline.get_width() // 2 + 1, height))
    screen.blit(text_outline, (WIDTH // 2 - text_outline.get_width() // 2, height - 1))
    screen.blit(text_outline, (WIDTH // 2 - text_outline.get_width() // 2, height + 1))
    screen.blit(rendered_text, (WIDTH // 2 - rendered_text.get_width() // 2, height))

def outline_text_w_box(screen, text, height, width=0) :
    text_outline = FONT.render(text, True, OUTLINE_COLOR)
    rendered_text = FONT.render(text, True, WHITE)

    screen.blit(text_outline, (WIDTH // 2 - text_outline.get_width() // 2 - 1 + width, height))
    screen.blit(text_outline, (WIDTH // 2 - text_outline.get_width() // 2 + 1 + width, height))
    screen.blit(text_outline, (WIDTH // 2 - text_outline.get_width() // 2 + width, height - 1))
    screen.blit(text_outline, (WIDTH // 2 - text_outline.get_width() // 2 + width, height + 1))
    screen.blit(rendered_text, (WIDTH // 2 - rendered_text.get_width() // 2 + width, height))

    button_rect = pygame.Rect(WIDTH // 2 - rendered_text.get_width() // 2 - 10 + width, height - 7, rendered_text.get_width() + 20, 40)
    pygame.draw.rect(screen, (255, 255, 255, 0), button_rect, 1)

    return button_rect

def edit_settings(screen) :
    running = True
    while running:
        # Handles events, This is where all mouse and keyboard inputs will be
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        screen.fill(WHITE)
        screen.blit(background_image, (0, 0))

        outline_text(screen, "This is where you can edit settings and settings are saved here.", 300)

        outline_text(screen, "Hit X to go back.", 350)

        pygame.display.flip()