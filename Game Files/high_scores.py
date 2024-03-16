import pygame
import settings as s
#from settings import WIDTH, HEIGHT, WHITE, BLACK, FONT



background_image = pygame.image.load("Game Files/assets/images/menubackground.jpg")
background_image = pygame.transform.scale(background_image, (s.WIDTH, s.HEIGHT))


# Font initialization
font = pygame.font.Font(None, 36)  # You can adjust the font size as needed
def load_high_score():
    try:
        with open("high_scores.txt", "r") as file:
         scores_str = file.read()  # Read the entire content of the file
         scores_list = scores_str.split('\n')  # Split the string into a list of scores
         scores_int = [int(score) for score in scores_list if score.strip()]  # Convert each score string to an integer
         return scores_int
    except FileNotFoundError:
        return 0

def save_high_score(score):
    # Read existing high scores from the file
    try:
        with open("high_score.txt", "r") as file:
            # Read the contents of the file and parse scores
            high_scores = [int(line.strip()) for line in file.readlines()]
    except FileNotFoundError:
        high_scores = []

    # Add the new score to the list
    high_scores.append(score)
    
    # Sort the high scores in descending order
    high_scores.sort(reverse=True)
    
    # Keep only the top 5 scores
    high_scores = high_scores[:5]

    # Write the updated high scores back to the file
    with open("high_score.txt", "w") as file:
        for s in high_scores:
            file.write(str(s) + "\n")


def view_high_score(screen):
     running = True
     while running:
        # Handles events, This is where all mouse and keyboard inputs will be
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        screen.fill(s.WHITE)
        screen.blit(background_image, (0, 0))
        try:
            with open("high_score.txt", "r") as file:
                high_score_content = file.read()
                s.outline_text(screen, high_score_content, 300)
        except FileNotFoundError:
            s.outline_text(screen, "No high score recorded", 300)

        pygame.display.flip()
    # Example usage of destroy_asteroid function
# Call destroy_asteroid whenever an asteroid is destroyed