import pygame
import settings as s
import utilities as u
from question import *
TRANSPARENT = (0, 0, 0, 0)

background_image = pygame.image.load("Game Files/assets/images/menubackground.jpg")
background_image = pygame.transform.scale(background_image, (s.WIDTH, s.HEIGHT))

def edit_questions(screen) :
    running = True
    selectedSeries = "ACM Ethics"
    selectedOption = 0
    new_series_name = ""
    enter_new_series = False
    selected_series_rect = None

    while running:
        # Handles events, This is where all mouse and keyboard inputs will be
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                    if option_rect.collidepoint(event.pos):
                        if selectedOption == 1:
                            selectedOption = 0
                        else:
                            selectedOption = 1
                    elif new_series_rect.collidepoint(event.pos):
                        enter_new_series = True
            # Handle text input events
            elif event.type == pygame.KEYDOWN:
                if enter_new_series:
                    if event.key == pygame.K_BACKSPACE:
                        new_series_name = new_series_name[:-1]  # Remove last character
                    elif event.key == pygame.K_RETURN:
                        # Handle confirmation of new series name (e.g., save to file, etc.)
                        print("New series name:", new_series_name)
                        add_new_series(new_series_name)
                        enter_new_series = False
                    elif event.key == pygame.K_ESCAPE:
                        enter_new_series = False
                        new_series_name = ""
                    else:
                        new_series_name += event.unicode  # Append typed character to series name

        screen.fill(TRANSPARENT)
        screen.blit(background_image, (0, 0)) 
        
        load_questions("Game Files/data/questions.json", selectedSeries)
        u.outline_text(screen, f"Edit questions for {selectedSeries}", 10, s.FONT, -265)
        u.outline_text(screen, "Enter Question:", 50, s.FONT, -130)
        u.outline_text(screen, "Choose Question Type:", 255, s.FONT, -90)

        # Next button
        next_button_rect = u.outline_text_w_box(screen, "Next", 10, s.FONT, 405)
        # Back Button
        back_button_rect = u.outline_text_w_box(screen, "Back", 10, s.FONT, 325)
        # Save Button
        save_button_rect = u.outline_text_w_box(screen, "Save", 10, s.FONT, 243)
        # New Button
        new_button_rect = u.outline_text_w_box(screen, "New Question", 10, s.FONT, 106)
        # New Series
        new_series_rect = u.outline_text_w_box(screen, "New Series", 550, s.FONT, -340)

        # Series Box
        left_box = pygame.Rect(10, 50, 200, 480)
        pygame.draw.rect(screen, s.WHITE, left_box, 2)  # Draw left box with white outline
        
        # Display series list
        series_y = 80
        series_list = get_series_list()
        
        for series in series_list:
            offset = len(series)
            series_rect = u.outline_text(screen, series, series_y, s.FONT, -330 - offset)
            if series_rect.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
                selectedSeries = series  # Change selected series if clicked
                selected_series_rect = series_rect
            series_y += 40

        # Underline the selected series
        if selected_series_rect:
            underline_rect = pygame.Rect(selected_series_rect.left, selected_series_rect.bottom - 2, selected_series_rect.width, 2)
            pygame.draw.rect(screen, (255, 255, 255), underline_rect)
        # Initial underline for ACM Ethics
        else:
            pygame.draw.line(screen, (255, 255, 255), (33, 111), (187, 111), 2)

        # Render text input box for new series name
        if enter_new_series:
            u.outline_text_w_box(screen, new_series_name, series_y, s.FONT, -340)
        


        # Question Box
        top_right_box = pygame.Rect(220, 80, 670, 160)
        pygame.draw.rect(screen, s.WHITE, top_right_box, 2)  # Draw top right box with white outline

        

        # Choice Box, 0 = multiple choice, 1 = true/false
        if selectedOption == 0:
            u.outline_text_w_box(screen, "Multiple Choice", 255, s.FONT, 160)
            option_rect = u.outline_text(screen, "True or False", 255, s.FONT, 350)
            
            u.outline_text(screen, "Enter Choices:", 290, s.FONT, -140)
            bottom_right_box_1 = pygame.Rect(220, 320, 670, 40)
            bottom_right_box_2 = pygame.Rect(220, 362, 670, 40)
            bottom_right_box_3 = pygame.Rect(220, 404, 670, 40)
            bottom_right_box_4 = pygame.Rect(220, 446, 670, 40)

            pygame.draw.rect(screen, s.WHITE, bottom_right_box_1, 2)
            pygame.draw.rect(screen, s.WHITE, bottom_right_box_2, 2)
            pygame.draw.rect(screen, s.WHITE, bottom_right_box_3, 2)
            pygame.draw.rect(screen, s.WHITE, bottom_right_box_4, 2)

            u.outline_text(screen, "Enter Correct Answer:", 510, s.FONT, -100)
            bottom_right_box_5 = pygame.Rect(220, 550, 670, 40)
            pygame.draw.rect(screen, s.WHITE, bottom_right_box_5, 2)

        if selectedOption == 1:
            u.outline_text_w_box(screen, "True or False", 255, s.FONT, 350)
            u.outline_text(screen, "Enter Choices:", 290, s.FONT, -140)
            option_rect = u.outline_text(screen, "Multiple Choice", 255, s.FONT, 160)

        pygame.display.flip()