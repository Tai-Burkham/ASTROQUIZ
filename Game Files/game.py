import pygame

# Constants
BLACK = (0, 0, 0)



def game(screen):
    game_over = False
    global score, health

    clock = pygame.time.Clock()
    
    # Game loop
    while not game_over:
        # Handle events, This is where all mouse and keyboard inputs will be
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    game_over = True

        screen.fill(BLACK)

        # Update game logic
        # interactions with astroids between ship



        # Draw everything
        



        pygame.display.flip()
        clock.tick(30)