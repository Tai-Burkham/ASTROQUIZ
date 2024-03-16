import pygame
import settings as s
#from settings import WIDTH, HEIGHT, WHITE, BLACK, FONT



#background_image = pygame.image.load("Game Files/assets/images/menubackground.jpg")
#background_image = pygame.transform.scale(background_image, (s.WIDTH, s.HEIGHT))


# Font initialization
font = pygame.font.Font(None, 36)  # You can adjust the font size as needed
def load_high_score(screen):
    try:
        with open("high_score.txt", "r") as file:
            return int(file.read())
    except FileNotFoundError:
        return 0

def save_high_score(score):
    with open("high_score.txt", "w") as file:
        file.write(str(score))

# Example usage of destroy_asteroid function
# Call destroy_asteroid whenever an asteroid is destroyed