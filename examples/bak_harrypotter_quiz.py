import os
import sys
import time
from PIL import Image, ImageDraw, ImageFont
from gpiozero import Button
sys.path.append('../lib')  # Path to Waveshare library
sys.path.append('/home/pi/e-Paper/RaspberryPi_JetsonNano/python/lib')  # Adjust path as needed
from waveshare_epd import epd2in7b_V2
from openai import OpenAI
from dotenv import load_dotenv
import ast
import sys
import image_generator as ig


# Load environment variables from .env file
load_dotenv()

# Set OpenAI API key
client = OpenAI(api_key=os.getenv("OPENAI_KEY"))


# Setup
epd = epd2in7b_V2.EPD()
epd.init()
epd.Clear()

FONT = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 12)
WIDTH, HEIGHT = epd.width, epd.height

# Buttons
btn1 = Button(5, pull_up=True)   # KEY1
btn2 = Button(6, pull_up=True)   # KEY2
btn3 = Button(13, pull_up=True)  # KEY3
btn4 = Button(19,pull_up=True)  # KEY4

# Generate questions
def generate_questions(topic, question_count, difficulty="medium", options=4):
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "user",
                "content": (
                    f"Generate a list of {question_count} {topic} trivia questions at {difficulty} difficulty in the following Python format — "
                    f"output only valid Python code starting exactly with 'questions = [...]'.\n\n"
                    f"# Format: questions = [\n"
                    f"#     (question_text, [{', '.join([f'option{i+1}' for i in range(options)])}], correct_index),\n"
                    f"#     ...\n"
                    f"# ]\n\n"
                    f"Each question must have {options} options, and the correct_index (0–{options-1}) must match the correct answer.\n"
                    "Do NOT include any explanations, comments, markdown formatting, or backticks — only output the Python list."
                )
            }
        ]
    )

    # Get raw response content
    raw_code = response.choices[0].message.content.strip()

    # Remove markdown code block wrappers if present
    if raw_code.startswith("```"):
        raw_code = raw_code.strip("`").strip()
        if raw_code.lower().startswith("python"):
            raw_code = raw_code[len("python"):].strip()

    # Now check and extract the list
    if raw_code.startswith("questions ="):
        questions_list_code = raw_code[len("questions ="):].strip()
        questions = ast.literal_eval(questions_list_code)
    else:
        raise ValueError("Expected response to start with 'questions ='")
    
    return questions

def wrap_text(text, font, max_width):
    words = text.split()
    lines = []
    line = ""
    for word in words:
        test_line = line + word + " "
        width, _ = font.getsize(test_line)
        if width <= max_width:
            line = test_line
        else:
            lines.append(line.strip())
            line = word + " "
    if line:
        lines.append(line.strip())
    return lines

def show_text(lines):
    image = Image.new('1', (WIDTH, HEIGHT), 255)
    draw = ImageDraw.Draw(image)
    y = 0
    for line in lines:
        wrapped = wrap_text(line, FONT, WIDTH)
        for subline in wrapped:
            if y + 20 > HEIGHT:
                break  # Prevent drawing off-screen
            draw.text((0, y), subline, font=FONT, fill=0)
            y += 20
    epd.display(epd.getbuffer(image), epd.getbuffer(image))

def wait_for_button():
    while True:
        if btn1.is_pressed: return 0
        if btn2.is_pressed: return 1
        if btn3.is_pressed: return 2
        if btn4.is_pressed: return 3
        time.sleep(0.1)

# Function for AI to generate conclusion based on score
def generate_conclusion(percentage, topic="Harry Potter"):
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "user",
                "content": (
                    f"Generate a conclusion for a {topic} quiz with score {percentage} percent. "
                    "Be extremely sassy but keep it very short"
                )
            }
        ]
    )
    return response.choices[0].message.content.strip()


# Function to show intro
def show_intro():
    intro_text = [
        "Welcome to the Harry Potter Quiz!",
        "Test your knowledge of the wizarding world.",
        "Press KEY1 to start, KEY2 to exit."
    ]
    show_text(intro_text)
    while True:
        if btn1.is_pressed:
            break
        elif btn2.is_pressed:
            epd.sleep()
            sys.exit("Exiting the quiz.")


# Function to start new game
def start_game(topic,questions):
    score = 0
    q_index = 0


    # # Generate image for the topic
    # # image_path = f"/home/pi/rpi-screen/gen_quiz_image.bmp"
    # ig.generate_image(topic, image_path)
    # # Crop and resize the image for display
    # ig.crop_image_3_2(image_path, image_path)
    # ig.resize_image(image_path, image_path)
    # # Convert to 4-bit bitmap format
    # ig.convert_to_4bit(image_path, image_path)
    # # Display the image on the e-Paper display
    # image_path = '/home/pi/rpi-screen/ai_gen_image_4bit.bmp'
    # ig.display_image(image_path)
    # # Wait for button press to continue
    # while True:
    #     if btn1.is_pressed:
    #         break

    while q_index < len(questions):
        
        # Display Questions
        q, options, correct = questions[q_index]
        show_text([f"Q{q_index+1}: {q}"] + [f"{i+1}. {opt}" for i, opt in enumerate(options)])
        choice = wait_for_button()
        
        if choice == correct:
            score += 1
            show_text(["Correct!", "", "Next question..."])
        else:
            show_text(["Incorrect!", f"Correct was: {options[correct]}", "", "Next question..."])
        time.sleep(2)
        q_index += 1

    return score



#### If name == "main":
if __name__ == "__main__":

    # Generate questions
    topic = "Harry Potter"
    question_count = 3
    difficulty = "medium"

    # Show intro
    show_intro()

    questions = generate_questions(topic, question_count, difficulty, options=3)

    # Start the game
    score = start_game(topic,questions)

    # Show score text
    percentage = (score / len(questions)) * 100
    conclusion = generate_conclusion(percentage, topic)
    show_text([
        f"Score: {score}/{len(questions)}, {percentage:.0f}%",
        conclusion,
        "Play again? KEY1 to start a new game, KEY2 to exit",
    ])
    # Wait for button press to restart or exit
    while True:
        if btn1.is_pressed:
            # Restart game
            questions = generate_questions(topic, question_count, difficulty, options=3)
            score = start_game(questions)
            percentage = (score / len(questions)) * 100
            conclusion = generate_conclusion(percentage)
            show_text([
                "Quiz Complete!",
                f"Your score: {score}/{len(questions)}",
                f"Percentage: {percentage:.1f}%",
                conclusion,
                "Play again? KEY1 to start a new game, KEY2 to exit",
            ])
        elif btn2.is_pressed:
            break
        time.sleep(0.1)


    time.sleep(7)
    epd.sleep()
