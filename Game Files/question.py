import json
import random
import pygame
import settings as s
import utilities as u

def load_questions(filename, series):
    with open(filename, "r") as file:
        questions_data = json.load(file)
    return questions_data[series]

def get_series_list(filename="Game Files/data/questions.json"):
    with open(filename, "r") as file:
        data = json.load(file)
    
    series_names = list(data.keys())
    return series_names

def add_new_series(name, filename="Game Files/data/questions.json"):
    # Load existing JSON data
    with open(filename, "r") as file:
        data = json.load(file)

    # Add a new key-value pair
    data[name] = []

    # Save the updated JSON data back to the file
    with open(filename, "w") as file:
        json.dump(data, file, indent=4)

    print(f"New series '{name}' added to questions.json") 

def edit_question_field(new_question, index, series, filename="Game Files/data/questions.json"):
    with open("Game Files/data/questions.json", "r") as file:
        data = json.load(file)

    data[series][index]["question"] = new_question

    with open("Game Files/data/questions.json", "w") as file:
        json.dump(data, file, indent=4)
      
def delete_question_from_series(index, series, filename="Game Files/data/questions.json"):
    with open("Game Files/data/questions.json", "r") as file:
        data = json.load(file)

    del data[series][index]

    with open("Game Files/data/questions.json", "w") as file:
        json.dump(data, file, indent=4)

def new_question(series, filename="Game Files/data/questions.json"):
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

def change_question_type(type, index, series, filename="Game Files/data/questions.json"):
    with open("Game Files/data/questions.json", "r") as file:
        data = json.load(file)

    if type == 0:
        data[series][index]["type"] = "multiple-choice"
    elif type == 1:
        data[series][index]["type"] = "true-false"
    
    with open("Game Files/data/questions.json", "w") as file:
        json.dump(data, file, indent=4)

def change_correct_answer(answer, index, series, filename="Game Files/data/questions.json"):
    with open("Game Files/data/questions.json", "r") as file:
        data = json.load(file)

    data[series][index]["correct_answer"] = answer

    with open("Game Files/data/questions.json", "w") as file:
        json.dump(data, file, indent=4)

def edit_answer_choice(answer, choice_index, index, series):
    with open("Game Files/data/questions.json", "r") as file:
        data = json.load(file)

    data[series][index]["options"][choice_index] = answer

    with open("Game Files/data/questions.json", "w") as file:
        json.dump(data, file, indent=4)
        
def display_question(screen, questions):
    # Choose a random question
    question_data = random.choice(questions)
    question = question_data["question"]
    type = question_data["type"]
    if type == "multiple-choice":
        choices = question_data["options"]

    # Font settings
    font = pygame.font.Font(None, 36)
    small_font = pygame.font.Font(None, 24)

    num_choices = len(choices) if type == "multiple-choice" else 2
    question_box_height = 200 + num_choices * 50  # Base height + height for each choice

    question_box_width = 800
    
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

    # Render the options
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