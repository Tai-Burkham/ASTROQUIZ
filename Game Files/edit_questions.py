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
    enter_question_text = False
    selected_series_rect = None
    question_index = 0
    num_of_questions = 0
    true_box = u.outline_text(screen, "", -100, s.FONT, -100)
    false_box = u.outline_text(screen, "", -100, s.FONT)

    while running:
        # Handles events, This is where all mouse and keyboard inputs will be
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if option_rect.collidepoint(event.pos):
                    if selectedOption == 1:
                        change_question_type(0, question_index, selectedSeries)
                    else:
                        change_question_type(1, question_index, selectedSeries)
                elif new_series_rect.collidepoint(event.pos):
                    enter_new_series = True
                elif next_button_rect.collidepoint(event.pos) and question_index < num_of_questions - 1:
                    question_index += 1
                elif back_button_rect.collidepoint(event.pos) and question_index > 0:
                    question_index -= 1
                elif remove_button_rect.collidepoint(event.pos) and num_of_questions > 0:
                    delete_question_from_series(question_index, selectedSeries)
                elif new_button_rect.collidepoint(event.pos):
                    new_question(selectedSeries)
                elif true_box.collidepoint(event.pos) and (questions[question_index]["correct_answer"] == "False" or questions[question_index]["correct_answer"] == ""):
                    change_correct_answer("True", question_index, selectedSeries)
                elif false_box.collidepoint(event.pos) and (questions[question_index]["correct_answer"] == "True" or questions[question_index]["correct_answer"] == ""):
                    change_correct_answer("False", question_index, selectedSeries)

                # right click
                if event.button == 3:
                    if question_box_rect.collidepoint(event.pos):
                        enter_question_text = True

            # Handle text input events
            elif event.type == pygame.KEYDOWN:
                if enter_new_series:
                    if event.key == pygame.K_BACKSPACE:
                        new_series_name = new_series_name[:-1]  # Remove last character
                    elif event.key == pygame.K_RETURN:
                        add_new_series(new_series_name)
                        enter_new_series = False
                    elif event.key == pygame.K_ESCAPE:
                        enter_new_series = False
                        new_series_name = ""
                    else:
                        new_series_name += event.unicode  # Append typed character to series name
                if enter_question_text:
                    original_text = question_text
                    if event.key == pygame.K_BACKSPACE:
                        question_text = question_text[:-1]  # Remove last character
                    elif event.key == pygame.K_RETURN:
                        edit_question_field(question_text, question_index, selectedSeries)
                        enter_question_text = False
                    elif event.key == pygame.K_ESCAPE:
                        enter_question_text = False
                        question_text = original_text
                    else:
                        question_text += event.unicode

        screen.fill(TRANSPARENT)
        screen.blit(background_image, (0, 0)) 

        questions = load_questions("Game Files/data/questions.json", selectedSeries)
        num_of_questions = len(questions)
        if num_of_questions <= 0:
            new_question(selectedSeries)
        u.outline_text(screen, f"Edit questions for {selectedSeries}", 10, s.FONT, -265)
        u.outline_text(screen, f"Enter Question: ({question_index}/{num_of_questions})", 50, s.FONT, -100 if question_index < 10 else -93)
        u.outline_text(screen, "Choose Question Type:", 255, s.FONT, -90)

        # UI Buttons
        next_button_rect = u.outline_text_w_box(screen, "Next", 10, s.FONT, 405)
        back_button_rect = u.outline_text_w_box(screen, "Back", 10, s.FONT, 325)
        remove_button_rect = u.outline_text_w_box(screen, "Remove", 10, s.FONT, 224)
        new_button_rect = u.outline_text_w_box(screen, "New Question", 10, s.FONT, 69)
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
                question_index = 0
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
            bottom_right_boxes = []  # List to hold the rectangles
            for i in range(1, 5):  # Create bottom right boxes and store their rectangles in the list
                bottom_right_box = pygame.Rect(220, 320 + (i - 1) * 42, 670, 40)
                bottom_right_boxes.append(bottom_right_box)
                pygame.draw.rect(screen, s.WHITE, bottom_right_box, 2)

            u.outline_text(screen, "Enter Correct Answer:", 510, s.FONT, -100)
            bottom_right_box_5 = pygame.Rect(220, 550, 670, 40)
            pygame.draw.rect(screen, s.WHITE, bottom_right_box_5, 2)

        if selectedOption == 1:
            u.outline_text_w_box(screen, "True or False", 255, s.FONT, 350)
            option_rect = u.outline_text(screen, "Multiple Choice", 255, s.FONT, 160)

            u.outline_text(screen, "Answer", 290, s.FONT, -140)
            true_box = u.outline_text(screen, "True", 340, s.FONT, -100)
            false_box = u.outline_text(screen, "False", 340, s.FONT)

        # Display the questions from the selected series in the top right box
        if questions:
            if not enter_question_text:
                question_text = questions[question_index]["question"]  # Display the first question
            question_box_rect = top_right_box
            question_surface = u.render_textrect(question_text, s.FONT, question_box_rect.inflate(-20, -20), s.WHITE, TRANSPARENT)
            screen.blit(question_surface, question_box_rect.inflate(-20, -20).topleft)

            if questions[question_index]["type"] == "multiple-choice":
                selectedOption = 0
            else:
                selectedOption = 1

            # Display the choices in the bottom right boxes
            if selectedOption == 0:
                for i, option in enumerate(questions[question_index]["options"]):
                    choice_box_rect = bottom_right_boxes[i]
                    choice_surface = u.render_textrect(option, s.FONT_SMALL, choice_box_rect.inflate(-20, -20), s.WHITE, TRANSPARENT)
                    screen.blit(choice_surface, choice_box_rect.inflate(-20, -20).topleft)
            
                correct_text = questions[question_index]["correct_answer"]
                correct_box_rect = bottom_right_box_5
                correct_box_surface = u.render_textrect(correct_text, s.FONT_SMALL, correct_box_rect.inflate(-20, -20), s.WHITE, TRANSPARENT)
                screen.blit(correct_box_surface, correct_box_rect.inflate(-20, -20).topleft)
            
            if selectedOption == 1:
                if questions[question_index]["correct_answer"] == "True":
                    correct_box = pygame.Rect(300, 330, 100, 50)
                else:
                    correct_box = pygame.Rect(400, 330, 100, 50)
                pygame.draw.rect(screen, s.WHITE, correct_box, 2)


        pygame.display.flip()