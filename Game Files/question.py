"""
File: question.py
Author: Calvin Leavy, Ahmed Krubally, Michelle Orro, Tailor Burkham

Description:
This file contains functions for editing questions including: load_questions,
get_series_list, add_new_series, edit_question_field, delete_question_from_series,
new_question, change_question_type, change_correct_answer, and edit_answer_choice.
It also displays questions during gameplay and handles answering the question.

"""
import json
import random
import pygame
import settings as s
import utilities as u

def load_questions(filename, series):
    """
    Load questions data from a JSON file.

    Args:
        filename (str): The name of the JSON file.
        series (str): The name of the question series.

    Returns:
        list: The list of questions data.
    """
    with open(filename, "r") as file:
        questions_data = json.load(file)
    return questions_data[series]

def get_series_list(filename="Game Files/data/questions.json"):
    """
    Get the list of question series from a JSON file.

    Args:
        filename (str, optional): The name of the JSON file. Defaults to "Game Files/data/questions.json".

    Returns:
        list: The list of question series.
    """
    with open(filename, "r") as file:
        data = json.load(file)
    
    series_names = list(data.keys())
    return series_names

def add_new_series(name, filename="Game Files/data/questions.json"):
    """
    Add a new question series to a JSON file.

    Args:
        name (str): The name of the new series.
        filename (str, optional): The name of the JSON file. Defaults to "Game Files/data/questions.json".

    Returns:
        None
    """
    # Load existing data
    with open(filename, "r") as file:
        data = json.load(file)

    # Add a new key-value pair
    data[name] = []

    # Save the updated data back to the file
    with open(filename, "w") as file:
        json.dump(data, file, indent=4)

    print(f"New series '{name}' added to questions.json") 

def edit_question_field(new_question, index, series):
    """
    Edits data in the question field

    Args:
        new_question (str): The new question data to be added.
        index (int): The index for the question to be edited.
        series (str): The name of the series the question is being edited.

    Returns:
        None
    """

    with open("Game Files/data/questions.json", "r") as file:
        data = json.load(file)

    data[series][index]["question"] = new_question

    with open("Game Files/data/questions.json", "w") as file:
        json.dump(data, file, indent=4)
      
def delete_question_from_series(index, series):
    """
    Deletes an entire question from a series

    Args:
        index (int): The index for the question to be deleted.
        series (str): The name of the series the question is being deleted.

    Returns:
        None
    """

    with open("Game Files/data/questions.json", "r") as file:
        data = json.load(file)

    del data[series][index]

    with open("Game Files/data/questions.json", "w") as file:
        json.dump(data, file, indent=4)

def new_question(series):
    """
    Creates a new_question in a series and fills it with default data

    Args:
        series (str): The name of the series the new question is added

    Returns:
        None
    """

    with open("Game Files/data/questions.json", "r") as file:
        data = json.load(file)

    new_question = {
        "type": "multiple-choice",
        "question": "Right click on boxes to edit. Enter your question here. Choose the type of question below and enter in the possible choices for multiple choice and select the correct answer or select the correct answer for true and false.",
        "options": ["", "", "", ""],
        "correct_answer": ""
    }

    data[series].append(new_question)

    with open("Game Files/data/questions.json", "w") as file:
        json.dump(data, file, indent=4)

def change_question_type(type, index, series):
    """
    Changes the type of question in the series

    Args:
        type (int): Type of question True/False(1) or Multiple Choice(0)
        index (int): The index for the question to be edited.
        series (str): The name of the series the question is being edited.

    Returns:
        None
    """

    with open("Game Files/data/questions.json", "r") as file:
        data = json.load(file)

    if type == 0:
        data[series][index]["type"] = "multiple-choice"
    elif type == 1:
        data[series][index]["type"] = "true-false"
    
    with open("Game Files/data/questions.json", "w") as file:
        json.dump(data, file, indent=4)

def change_correct_answer(answer, index, series):
    """
    Changes the correct answer for a question in the series

    Args:
        answer (str): The answer data for the question
        index (int): The index for the question to be edited.
        series (str): The name of the series the question is being edited.

    Returns:
        None
    """

    with open("Game Files/data/questions.json", "r") as file:
        data = json.load(file)

    data[series][index]["correct_answer"] = answer

    with open("Game Files/data/questions.json", "w") as file:
        json.dump(data, file, indent=4)

def edit_answer_choice(answer, choice_index, index, series):
    """
    Edits the answer choices for a question in the series

    Args:
        answer (str): The answer data for the question
        choice_index (int): for multiple choice, selects which choice is being edited
        index (int): The index for the question to be edited.
        series (str): The name of the series the question is being edited.

    Returns:
        None
    """

    with open("Game Files/data/questions.json", "r") as file:
        data = json.load(file)

    data[series][index]["options"][choice_index] = answer

    with open("Game Files/data/questions.json", "w") as file:
        json.dump(data, file, indent=4)
        
def display_question(screen, questions):
    """
    Display a randomly selected question on the screen.

    Args:
        screen: The Pygame display surface.
        questions (list): The list of questions data.

    Returns:
        bool: True if the selected answer is correct, False otherwise.
    """

    # Choose a random question
    question_data = random.choice(questions)
    question = question_data["question"]
    type = question_data["type"]
    if type == "multiple-choice":
        choices = question_data["options"]

    # Font settings
    font = pygame.font.Font(None, 36)
    small_font = pygame.font.Font(None, 24)

    # Sets question box size based off question data
    num_choices = len(choices) if type == "multiple-choice" else 2
    question_box_height = 200 + num_choices * 50 

    question_box_width = 800
    
    # Centers question box
    question_box_x = (s.WIDTH - question_box_width) // 2
    question_box_y = (s.HEIGHT - question_box_height) // 2
    
    question_box_rect = pygame.Rect(question_box_x, question_box_y, question_box_width, question_box_height)
    
    # Draw white outline
    outline_rect = question_box_rect.inflate(2, 2)  # Inflate the rectangle to create an outline
    pygame.draw.rect(screen, s.WHITE, outline_rect)

    # Fill the question box with a background color
    background_color = s.BLACK
    pygame.draw.rect(screen, background_color, question_box_rect)

    # Render the question text with word wrapping
    question_surface = u.render_textrect(question, font, question_box_rect.inflate(-20, -20), s.WHITE, s.BLACK)
    screen.blit(question_surface, question_box_rect.inflate(-20, -20).topleft)

    # Render the answer boxes
    option_rects = []
    y = 200
    if type == "multiple-choice":
        for option in choices:
            option_rect = u.outline_text_w_box(screen, option, y, small_font)
            option_rects.append(option_rect)
            y += 50
    else:
        y += 100
        option_rect = u.outline_text_w_box(screen, "True", y, font)
        option_rects.append(option_rect)
        y += 50
        
        option_rect = u.outline_text_w_box(screen, "False", y, font)
        option_rects.append(option_rect)
        y += 50

    pygame.display.flip()

    # Wait for player input
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for option_rect, option_text in zip(option_rects, choices if type == "multiple-choice" else ["True", "False"]):
                    if option_rect.collidepoint(event.pos):
                        # Check the correctness of the answer and return
                        if type == "multiple-choice":
                            selected_option_text = option_text
                        else:
                            selected_option_text = "True" if option_text == "True" else "False"

                        return selected_option_text == question_data["correct_answer"]