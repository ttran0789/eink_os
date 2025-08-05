import os
import sys
import time
from PIL import Image, ImageDraw, ImageFont
from gpiozero import Button
sys.path.append('../lib')  # Path to Waveshare library
sys.path.append('/home/pi/e-Paper/RaspberryPi_JetsonNano/python/lib')  # Adjust path as needed
from waveshare_epd import epd2in7_V2
from dotenv import load_dotenv
from openai import OpenAI
import ast

# Load environment variables from .env file
load_dotenv()

# Set OpenAI API key
client = OpenAI(api_key=os.getenv("OPENAI_KEY"))



# Setup Screen
epd = epd2in7_V2.EPD()
epd.init()
epd.Clear()

FONT = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 12)
WIDTH, HEIGHT = epd.width, epd.height

# Buttons
btn1 = Button(5, pull_up=True)   # KEY1
btn2 = Button(6, pull_up=True)   # KEY2
btn3 = Button(13, pull_up=True)  # KEY3
btn4 = Button(19,pull_up=True)  # KEY4

# Button callback functions
def wait_for_button():
    while True:
        if btn1.is_pressed: return 0
        if btn2.is_pressed: return 1
        if btn3.is_pressed: return 2
        if btn4.is_pressed: return 3
        time.sleep(0.1)

# Function to wrap text
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

# Add to test_wrapped
def add_to_text_array(text_array, text):
    if isinstance(text_array, list):
        text_array.append(text)
    else:
        raise ValueError("text_array must be a list.")
    return text_array

def show_text(lines):
    """Display multiple lines of text on the e-Paper screen in landscape orientation."""
    epd.init()
    epd.Clear()
    
    # Create a blank image in landscape (swap WIDTH and HEIGHT)
    image = Image.new('1', (HEIGHT, WIDTH), 255)
    draw = ImageDraw.Draw(image)
    
    y = 10
    line_height = FONT.getsize("A")[1] + 4  # Add some spacing
    for line in lines:
        if y + line_height > HEIGHT:
            break  # Prevent drawing off-screen
        draw.text((10, y), line, font=FONT, fill=0)
        y += line_height

    # Rotate the image to landscape
    image = image.rotate(90, expand=True)
    
    # Display the image
    epd.display(epd.getbuffer(image))
    epd.sleep()

# Function to show intro
def show_intro():
    # intro_text = [
    #     "Welcome to the Harry Potter Quiz! Test your knowledge of the wizarding world.",
    #     "",
    #     "Press KEY1 to start, KEY2 to exit."
    # ]
    intro_text = "Welcome to the Harry Potter Quiz! Test your knowledge of the wizarding world."
    wrapped = wrap_text(intro_text, FONT, HEIGHT)
    wrapped2 = add_to_text_array(wrapped, "")
    wrapped2 = add_to_text_array(wrapped, "Press KEY1 to start, KEY2 to exit.")
    show_text(wrapped2)
    while True:
        if btn1.is_pressed:
            break
        elif btn2.is_pressed:
            epd.sleep()
            sys.exit("Exiting the quiz.")


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




if __name__ == "__main__":

    ## Show INTRO
    # show_intro()



    ## SHOW QUESTIONS

    # Generate questions
    # questions = generate_questions("Harry Potter", 2, difficulty="easy", options=3)
    questions = [('What student wizard house is Harry Potter sorted into?', ['Hufflepuff', 'Gryffindor', 'Ravenclaw'], 1), ("Who is known as the 'Boy Who Lived'?", ['Neville Longbottom', 'Harry Potter', 'Draco Malfoy'], 1)]
    print(questions)

    # Loop through questions and write it out
    for q in questions:
        question_text, options, correct_index = q
        wrapped_question_number = f"Question {questions.index(q) + 1}:"
        wrapped_question = wrap_text(question_text, FONT, HEIGHT)
        wrapped_question = [wrapped_question_number] + wrapped_question
        wrapped_options = [wrap_text(option, FONT, HEIGHT) for option in options]

        # Combine question and options
        wrapped_lines = []
        if wrapped_question:
            wrapped_lines.append(f"{wrapped_question[0]}")
            wrapped_lines.extend(wrapped_question[1:])
        for idx, option in enumerate(wrapped_options, 1):
            for line in option:
                wrapped_lines.append(f"{idx}: {line}")
        wrapped_lines = add_to_text_array(wrapped_lines, "")
        show_text(wrapped_lines)
        
        # Sleep
        time.sleep(5)