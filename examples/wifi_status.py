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
import socket

# Load environment variables from .env file
load_dotenv()

# Set OpenAI API key
client = OpenAI(api_key=os.getenv("OPENAI_KEY"))




def get_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return None

def main():
    epd = epd2in7_V2.EPD()
    epd.init()
    epd.Clear()

    image = Image.new('1', (epd.width, epd.height), 255)
    draw = ImageDraw.Draw(image)

    font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf', 18)

    ip = get_ip()
    if ip:
        msg = f"Wi-Fi Connected\nIP: {ip}"
    else:
        msg = "No Wi-Fi Connection"

    draw.text((10, 50), msg, font=font, fill=0)
    epd.display(epd.getbuffer(image))
    epd.sleep()

if __name__ == "__main__":
    main()
