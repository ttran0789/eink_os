#\!/usr/bin/env python3
import os
import sys

# Calculate paths dynamically based on script location
script_dir = os.path.dirname(os.path.realpath(__file__))
epaper_root = "/home/pi/e-Paper/RaspberryPi_JetsonNano/python"
libdir = os.path.join(epaper_root, "lib")
examplesdir = os.path.join(epaper_root, "examples")

# Add paths if they exist
if os.path.exists(libdir):
    sys.path.insert(0, libdir)
if os.path.exists(examplesdir):
    sys.path.insert(0, examplesdir)

# Change to examples directory for relative file access
os.chdir(examplesdir)

# Now import and run
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
load_dotenv(os.path.join(examplesdir, ".env"))

# Set OpenAI API key
client = OpenAI(api_key=os.getenv("OPENAI_KEY"))

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
