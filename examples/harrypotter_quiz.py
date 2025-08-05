import os
import sys
import time
from PIL import Image, ImageDraw, ImageFont
from gpiozero import Button
sys.path.append('../lib')  # Path to Waveshare library
sys.path.append('/home/pi/e-Paper/RaspberryPi_JetsonNano/python/lib')  # Adjust path as needed
from waveshare_epd import epd2in7b_V2
import helper_quiz as hq
from openai import OpenAI
from dotenv import load_dotenv
import ast
import sys
import image_generator as ig


# Load environment variables from .env file
load_dotenv()

# Set OpenAI API key
client = OpenAI(api_key=os.getenv("OPENAI_KEY"))

#### If name == "main":
if __name__ == "__main__":

    topic = 'Profusionist'

    # Initialize the game
    hpq = hq.quizGame()


    # Settings
    hpq.topic = topic
    hpq.question_count = 4
    hpq.difficulty = "medium"

    # Show intro / Start Game
    # hpq.show_intro()









    # # TEST: Modify score and Show End
    # hpq.score=4
    # hpq.show_score()

    # # TEST: Display image 
    # fp = r'/home/pi/rpi-screen/images/ai_hp_image_resized_20250529_094532.bmp'
    # hpq.display_image_4bit(fp)


    # Override topic
    topic = "Senior dog (grey haired) black lab eating cookies"


    # TEST: Generate and show image
    imagepath = hpq.generate_4bit_image(topic)
    hpq.display_image_4bit(imagepath)
