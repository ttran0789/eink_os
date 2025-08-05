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
import image_generator as imgn

# Load environment variables from .env file
load_dotenv()

# Set OpenAI API key
client = OpenAI(api_key=os.getenv("OPENAI_KEY"))


class quizGame:
    def __init__(self):
        print("Initializing quiz game...")
        self.topic = "Harry Potter"
        self.question_count = 3
        self.difficulty = "hard"
        self.options = 3
        self.questions = []
        self.question_count = len(self.questions)
        self.current_question_index = 0
        self.score = 0
        self.init_buttons()
        self.init_screen()

    def init_buttons(self):
        # Buttons
        self.btn1 = Button(5, pull_up=True)   # KEY1
        self.btn2 = Button(6, pull_up=True)   # KEY2
        self.btn3 = Button(13, pull_up=True)  # KEY3
        self.btn4 = Button(19,pull_up=True)  # KEY4

    def init_screen(self):
        """Initialize the e-Paper screen."""
        self.epd = epd2in7_V2.EPD()
        self.epd.init()
        self.WIDTH, self.HEIGHT = self.epd.width, self.epd.height
        self.FONT = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 12)

    def load_questions(self, questions):
        """Load questions into the game."""
        self.questions = questions
        self.current_question_index = 0
        self.score = 0

    def show_text(self, lines):
        """Display multiple lines of text on the e-Paper screen in landscape orientation."""
        self.epd.init()
        self.epd.Clear()
        
        # Create a blank image in landscape (swap WIDTH and self.HEIGHT)
        image = Image.new('1', (self.HEIGHT, self.WIDTH), 255)
        draw = ImageDraw.Draw(image)
        
        y = 10
        line_height = self.FONT.getsize("A")[1] + 4
        for line in lines:
            if y + line_height > self.HEIGHT:
                break
            draw.text((10, y), line, font=self.FONT, fill=0)
            y += line_height
        # Rotate the image to landscape
        image = image.rotate(90, expand=True)
        # Display the image
        self.epd.display(self.epd.getbuffer(image))

        # Sleep
        self.epd.sleep()

    def quick_refresh(self, lines=["Hello world"]):
        # Quick refresh
        self.epd.init_Fast()
        # Drawing on the Vertical image
        Himage = Image.new('1', (self.epd.height, self.epd.width), 255)  # 255: clear the frame
        draw = ImageDraw.Draw(Himage)
        
        y = 10
        line_height = self.FONT.getsize("A")[1] + 4
        for line in lines:
            if y + line_height > self.epd.height:
                break
            draw.text((10, y), line, font=self.FONT, fill=0)
            y += line_height


        self.epd.display_Fast(self.epd.getbuffer(Himage))
        time.sleep(1)
        # Sleep
        self.epd.sleep()

    def wrap_text(self, text, font, max_width):
        """Wrap text to fit within the specified width."""
        words = text.split()
        lines = []
        line = ""
        for word in words:
            test_line = line + word + " "
            width, _ = self.FONT.getsize(test_line)
            if width <= max_width:
                line = test_line
            else:
                lines.append(line.strip())
                line = word + " "
        if line:
            lines.append(line.strip())
        return lines
    
    def add_to_text_array(self, text_array, text):
        """Add a text line to the text array."""
        if isinstance(text_array, list):
            text_array.append(text)
        else:
            raise ValueError("text_array must be a list.")
        return text_array
    
    def wait_for_button(self):
        """Wait for a button press and return the button index."""
        while True:
            if self.btn1.is_pressed: return 0
            if self.btn2.is_pressed: return 1
            if self.btn3.is_pressed: return 2
            if self.btn4.is_pressed: return 3
            time.sleep(0.1)

    def generate_questions(self, topic, question_count, difficulty="medium", options=4):
        """Generate trivia questions using OpenAI API."""
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

    def generate_4bit_image(self,topic=None):
        # Set topic if not provided
        if topic is None:
            topic = r"Harry Potter world artwork, not just related to Harry Potter character, but also to the whole Harry Potter world, with Hogwarts castle, magical creatures, OR other elements of the wizarding world. More so than just artwork of the characters, but also the world they live in, the magical creatures, the Hogwarts castle, and other elements of the wizarding world. The image should be colorful, vibrant, and capture the essence of the Harry Potter universe."

        timestamp = time.strftime("%Y%m%d_%H%M%S")
        filepath = f"/home/pi/rpi-screen/images/ai_hp_{timestamp}.bmp"
        filepath_new = f"/home/pi/rpi-screen/images/ai_hp_crop_{timestamp}.bmp"
        filepath_resized = f"/home/pi/rpi-screen/images/ai_hp_image_resized_{timestamp}.bmp"
        filepath_4bit = f"/home/pi/rpi-screen/images/ai_hp_4bit_{timestamp}.bmp"

        # Generate the image
        imgn.generate_image(topic, filepath)
        # Crop the image to 3:2 aspect ratio
        imgn.crop_image_3_2(filepath, filepath_new)
        # Resize image down to fit the e-Paper display: 264x176 pixels
        imgn.resize_image(filepath_new, filepath_resized)
        # # Function to display the image on the e-Paper display
        # self.display_image_4bit(filepath_resized)
        return filepath_resized

    def convert_show_image(self,filepath=None):
        """Convert and display an image on the e-Paper screen."""
        if filepath is None:
            filepath = r'/home/pi/rpi-screen/images/ai_hp_20250528_094243.bmp'
        # Crop the image to 3:2 aspect ratio
        filepath_new = filepath.replace(".bmp", "_crop.bmp")
        imgn.crop_image_3_2(filepath, filepath_new)
        # Resize image down to fit the e-Paper display: 264x176 pixels
        filepath_resized = filepath.replace(".bmp", "_resized.bmp")
        imgn.resize_image(filepath_new, filepath_resized)
        # Function to display the image on the e-Paper display
        self.display_image_4bit(filepath_resized)

    def display_image_4bit(self, filepath):
        """Display a 4-level grayscale image on the e-Paper screen."""
        self.epd.Init_4Gray()

        # Load and process image
        img = Image.open(filepath).convert('L')  # Convert to grayscale
        img = img.resize((self.epd.height, self.epd.width))

        # Map to 4 grayscale levels: 0, 85, 170, 255
        img = img.point(lambda x: 0 if x < 64 else 85 if x < 128 else 170 if x < 192 else 255, 'L')

        # Display directly
        self.epd.display_4Gray(self.epd.getbuffer_4Gray(img))
        time.sleep(2)
        self.epd.sleep()
        print(f"Image displayed on e-Paper display from {filepath}")
    
    def show_question(self, question):
        """Display a question and its options on the e-Paper screen."""
        question_text, options, correct_index = question
        wrapped_question_number = f"Question {self.current_question_index + 1}:"
        wrapped_question = self.wrap_text(question_text, self.FONT, self.HEIGHT)
        wrapped_question = [wrapped_question_number] + wrapped_question
        wrapped_options = [self.wrap_text(option, self.FONT, self.HEIGHT) for option in options]

        # Combine question and options
        wrapped_lines = []
        if wrapped_question:
            wrapped_lines.append(f"{wrapped_question[0]}")
            wrapped_lines.extend(wrapped_question[1:])
        # for idx, option in enumerate(wrapped_options, 1):
        #     for line in option:
        #         wrapped_lines.append(f"{idx}: {line}")

        # Combine questions and options, only show idx first instance if there are multiple lines
        for idx, option in enumerate(wrapped_options, 1):
            if len(option) > 1:
                wrapped_lines.append(f"{idx}: {option[0]}")
                for line in option[1:]:
                    wrapped_lines.append(f"   {line}")
            else:
                wrapped_lines.append(f"{idx}: {option[0]}")
        
        wrapped_lines = self.add_to_text_array(wrapped_lines, "")

        self.show_text(wrapped_lines)
    
    def show_score(self):
        """Display the final score on the e-Paper screen."""
        score_text = f"Your final score is: {self.score}/{self.question_count}"
        score_pct = (int(self.score / self.question_count * 100)) if self.question_count > 0 else 0

        # Commentary based on score percentage
        if score_pct >= 75:
            score_text += " - Well done! You are a true Harry Potter fan!"
            score_text += " - See your prize in the next screen!"
        elif score_pct >= 50:
            score_text += " - Good job! You know your Harry Potter trivia!"
        else:
            score_text += " - Keep practicing! You can improve your Harry Potter knowledge!"
        wrapped_score = self.wrap_text(score_text, self.FONT, self.HEIGHT)

        wrapped_score = self.add_to_text_array(text_array=wrapped_score, text="")

        if score_pct < 75:
            wrapped_score = self.add_to_text_array(text_array=wrapped_score, text="Play again?")
            wrapped_score = self.add_to_text_array(text_array=wrapped_score, text="Press KEY1 to restart, KEY2 to exit.")
            # Show text
            self.show_text(wrapped_score)
        else:
            self.show_text(wrapped_score)
            # Wait for any key to continue
            while True:
                if self.btn1.is_pressed or self.btn2.is_pressed or self.btn3.is_pressed or self.btn4.is_pressed:
                    # Generate image
                    fp_4bit_img = self.generate_4bit_image(topic=self.topic)
                        
                    # #### TEST: Display image 
                    # fp_4bit_img = r'/home/pi/rpi-screen/images/ai_hp_image_resized_20250529_094532.bmp'
                    # #### END TEST



                    # Show image
                    print(f'Filepath of 4bit image generated: {fp_4bit_img}')
                    self.display_image_4bit(fp_4bit_img)

                    # While True:
                    while True:
                        if self.btn1.is_pressed:
                            self.start_game()
                        elif self.btn2.is_pressed:
                            self.epd.sleep()
                            sys.exit("Exiting the quiz.")
        
        # Wait for a button press to exit
        while True:
            if self.btn1.is_pressed:
                self.start_game()
            elif self.btn2.is_pressed:
                self.epd.sleep()
                sys.exit("Exiting the quiz.")

    def show_intro(self):
        """Display the introduction text on the e-Paper screen."""
        intro_text = "Welcome to the Harry Potter Quiz! Test your knowledge of the wizarding world. Get 75% or better to win a prize!"
        wrapped = self.wrap_text(intro_text, self.FONT, self.HEIGHT)
        wrapped2 = self.add_to_text_array(wrapped, "")
        wrapped2 = self.add_to_text_array(wrapped2, "Press KEY1 to start, KEY2 to exit.")
        self.show_text(wrapped2)
        
        while True:
            if self.btn1.is_pressed:
                self.start_game()
            elif self.btn2.is_pressed:
                self.epd.sleep()
                sys.exit("Exiting the quiz.")
    
    def start_game(self):
        # Generate and load questions
        print("Generating questions...")
        self.questions = self.generate_questions(self.topic, self.question_count, self.difficulty, self.options)
        # Store questions to backup: CSV
        with open('questions_backup_{}.csv'.format(self.difficulty), 'a') as f:
            for question in self.questions:
                f.write(f"{question[0]},{','.join(question[1])},{question[2]}\n")

        print("Loading questions into the game...")
        self.load_questions(self.questions)

        # Start the quiz
        for self.current_question_index, question in enumerate(self.questions):
            self.show_question(question)
            print(f"Showing question {self.current_question_index + 1}...")
            selected_option = self.wait_for_button()
            print(f"Selected option: {selected_option + 1}")
            if selected_option == question[2]:
                self.score += 1
                self.quick_refresh([f"Correct! Your score is now {self.score}."])
                print("Correct answer!")
            else:
                message = f"Wrong! The correct answer was option {question[2] + 1}: {question[1][question[2]]}"
                wrapped = self.wrap_text(message, self.FONT, self.HEIGHT)
                self.quick_refresh(wrapped)
                print(f"Wrong answer! Correct answer was option {question[2] + 1}.")
        
        # Show final score
        self.show_score()
        print("Quiz completed. Showing final score...")




if __name__ == "__main__":

    # Initialize the quiz game
    print("Initializing the quiz game...")
    quiz = quizGame()

    # Show intro
    print("Showing intro...")
    # quiz.show_intro()