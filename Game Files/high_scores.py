import pygame
import settings as s
#from settings import WIDTH, HEIGHT, WHITE, BLACK, FONT

# Initialize score and asteroid destroyed counter variables
score = 0
asteroids_destroyed = 0

#background_image = pygame.image.load("Game Files/assets/images/menubackground.jpg")
#background_image = pygame.transform.scale(background_image, (s.WIDTH, s.HEIGHT))


# Font initialization
font = pygame.font.Font(None, 36)  # You can adjust the font size as needed

def view_High_Scores(screen) :
    global score, asteroids_destroyed  # Use global variables for score and asteroids_destroyed
    
    running = True
    while running:
        # Handles events, This is where all mouse and keyboard inputs will be
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_x:  # Add functionality to go back
                    return

       # screen.fill(s.WHITE)
       # screen.blit(background_image, (0, 0))
 
 # Display current score and asteroids destroyed
        score_text = font.render(f"Score: {score}", True, (255, 0, 0))
        screen.blit(score_text, (s.WIDTH - score_text.get_width() - 10, 10))  # Position score text at top right


       # pygame.display.flip()


# Function to handle asteroid destruction and score update
def destroy_asteroid():
    global score, asteroids_destroyed  # Use global variables for score and asteroids_destroyed
    score += 100  # Increase score by 100 when an asteroid is destroyed
    asteroids_destroyed += 1  # Increase asteroids_destroyed counter by 1 when an asteroid is destroyed

# Example usage of destroy_asteroid function
# Call destroy_asteroid whenever an asteroid is destroyed