#\!/usr/bin/env /home/pi/e-Paper/RaspberryPi_JetsonNano/python/examples/testenv/bin/python
import os
import sys
import subprocess

# Add the waveshare library path
sys.path.insert(0, "/home/pi/e-Paper/RaspberryPi_JetsonNano/python/lib")

# Add the examples directory for helper modules
sys.path.insert(0, "/home/pi/e-Paper/RaspberryPi_JetsonNano/python/examples")

# Change working directory to examples folder to ensure relative paths work
os.chdir("/home/pi/e-Paper/RaspberryPi_JetsonNano/python/examples")

# Import everything from the original script
import time
from PIL import Image, ImageDraw, ImageFont
from gpiozero import Button
from waveshare_epd import epd2in7b_V2
import helper_quiz as hq
from openai import OpenAI
from dotenv import load_dotenv
import ast
import image_generator as ig

# Load environment variables from .env file
load_dotenv()

# Set OpenAI API key
client = OpenAI(api_key=os.getenv("OPENAI_KEY"))

#### If name == "main":
if __name__ == "__main__":

    topic = "Profusionist"

    # Initialize the game
    hpq = hq.quizGame()

    # Settings
    hpq.topic = topic
    hpq.question_count = 4
    hpq.difficulty = "medium"

    # Override topic
    topic = "Senior dog (grey haired) black lab eating cookies"

    # TEST: Generate and show image
    imagepath = hpq.generate_4bit_image(topic)
    hpq.display_image_4bit(imagepath)
