import pygame
import utilities as u

# needed for font setting
pygame.init()

# Game Settings
WIDTH, HEIGHT = 900, 600
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
FONT = pygame.font.Font(None, 36)
FONT_SMALL = pygame.font.Font(None, 24)
TEXT_COLOR = (255, 255, 255)
TRANSPARENT = (0, 0, 0, 0)

back_button = pygame.Rect(50, 500, 100, 50)  # Adjust position and size as needed
save_button = pygame.Rect(200, 500, 100, 50)  # Adjust position and size as needed

background_image = pygame.image.load("Game Files/assets/images/menubackground.jpg")
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))

spaceship_1 = pygame.image.load("Game Files/assets/images/spaceship_1.png")
spaceship_1 = pygame.transform.scale(spaceship_1, (150,150))
spaceship_2 = pygame.image.load("Game Files/assets/images/spaceship_2.png")
spaceship_2 = pygame.transform.scale(spaceship_2, (150,150))
spaceship_3 = pygame.image.load("Game Files/assets/images/spaceship_3.png")
spaceship_3 = pygame.transform.scale(spaceship_3, (150,150))

ship_image_file = "Game Files/assets/images/spaceship_1.png" 
question_series = "ACM Ethics"
asteroid_count = 10

selected_ship = None 
questions_on = True
music_on = True
sound_on = True
hard_difficulty = False

def edit_settings(screen):
    global questions_on, music_on, sound_on, hard_difficulty, selected_ship, ship_image_file, save_button, back_button

    running = True
    while running:
        # Handles events, This is where all mouse and keyboard inputs will be
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    if ship_box_1.collidepoint(mouse_pos):
                        selected_ship = "ship1"
                        ship_image_file = "Game Files/assets/images/spaceship_1.png"
                    elif ship_box_2.collidepoint(mouse_pos):
                        selected_ship = "ship2"
                        ship_image_file = "Game Files/assets/images/spaceship_2.png"
                    elif ship_box_3.collidepoint(mouse_pos):
                        selected_ship = "ship3"
                        ship_image_file = "Game Files/assets/images/spaceship_3.png"
                
                    elif questions_on_rect.collidepoint(mouse_pos) and not questions_on:
                        questions_on = True
                    elif questions_off_rect.collidepoint(mouse_pos) and questions_on:
                        questions_on = False
                    elif sound_on_rect.collidepoint(mouse_pos) and not sound_on:
                        sound_on = True
                    elif sound_off_rect.collidepoint(mouse_pos) and sound_on:
                        sound_on = False
                    elif music_on_rect.collidepoint(mouse_pos) and not music_on:
                        music_on = True
                    elif music_off_rect.collidepoint(mouse_pos) and music_on:
                        music_on = False
                    elif hard_diff_rect.collidepoint(mouse_pos) and not hard_difficulty:
                        hard_difficulty = True
                    elif normal_diff_rect.collidepoint(mouse_pos) and hard_difficulty:
                        hard_difficulty = False

                    elif back_button.collidepoint(mouse_pos):
                    # Navigate back to the main page
                        running = False
                    elif save_button.collidepoint(mouse_pos):
                    # Save the current settings
                        with open('settings.txt', 'w') as f:
                            f.write(f'selected_ship={selected_ship}\n')
                            f.write(f'ship_image_file={ship_image_file}\n')

                        running = False

        screen.fill(WHITE)
        screen.blit(background_image, (0, 0))
        u.outline_text(screen, "Settings", 10, FONT, -390)

        # Ship Selection
        u.outline_text(screen, "Choose Ship Type", 50, FONT, -335)
        ship_box_1 = pygame.Rect(35, 85, 180, 180)
        ship_box_2 = pygame.Rect(265, 85, 180, 180)
        ship_box_3 = pygame.Rect(485, 85, 180, 180)

        pygame.draw.rect(screen, RED if selected_ship == "ship1" else WHITE, ship_box_1, 2)
        pygame.draw.rect(screen, RED if selected_ship == "ship2" else WHITE, ship_box_2, 2)
        pygame.draw.rect(screen, RED if selected_ship == "ship3" else WHITE, ship_box_3, 2)
        screen.blit(spaceship_1, (50, 100))
        screen.blit(spaceship_2, (275, 100))
        screen.blit(spaceship_3, (500, 100))

        save_button = u.outline_text_w_box(screen, "SAVE", 230, FONT, 290) 

        # Turn off Questions
        u.outline_text(screen, "Questions:", 300, FONT, -370)
        questions_on_rect = u.outline_text_w_box(screen, "ON", 300, FONT, -260) if questions_on else u.outline_text(screen, "ON", 300, FONT, -260)
        questions_off_rect = u.outline_text(screen, "OFF", 300, FONT, -190) if questions_on else u.outline_text_w_box(screen, "OFF", 300, FONT, -190)

        # Audio Settings
        u.outline_text(screen, "Music On:", 350, FONT, -377)
        music_on_rect = u.outline_text_w_box(screen, "ON", 350, FONT, -260) if music_on else u.outline_text(screen, "ON", 350, FONT, -260)
        music_off_rect = u.outline_text(screen, "OFF", 350, FONT, -190) if music_on else u.outline_text_w_box(screen, "OFF", 350, FONT, -190)

        u.outline_text(screen, "Sound On:", 400, FONT, -373)
        sound_on_rect = u.outline_text_w_box(screen, "ON", 400, FONT, -260) if sound_on else u.outline_text(screen, "ON", 400, FONT, -260)
        sound_off_rect = u.outline_text(screen, "OFF", 400, FONT, -190) if sound_on else u.outline_text_w_box(screen, "OFF", 400, FONT, -190)

        u.outline_text(screen, "Game Difficulty:", 450, FONT, -340)
        normal_diff_rect = u.outline_text_w_box(screen, "Normal", 450, FONT, -170) if not hard_difficulty else u.outline_text(screen, "Normal", 450, FONT, -170)
        hard_diff_rect = u.outline_text(screen, "Hard", 450, FONT, -70) if not hard_difficulty else u.outline_text_w_box(screen, "Hard", 450, FONT, -70)
     
        back_button = u.outline_text_w_box(screen, "BACK", 500, FONT, -370)

        pygame.display.flip()
