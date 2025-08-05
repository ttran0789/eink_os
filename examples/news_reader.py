import feedparser
from PIL import Image, ImageDraw, ImageFont
import time
import os
import sys
sys.path.append('../lib')  # Path to Waveshare library
from waveshare_epd import epd2in7b_V2
import RPi.GPIO as GPIO

# Buttons (adjust as needed)
BUTTONS = [5, 6, 13, 19]  # GPIO pins for KEY1–KEY4

GPIO.setmode(GPIO.BCM)
for btn in BUTTONS:
    GPIO.setup(btn, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Fonts
# FONT = ImageFont.load_default()
FONT = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 12)

# Init display
epd = epd2in7b_V2.EPD()
epd.init()
epd.Clear()

# Fetch headlines
def get_news(feed_url='https://rss.nytimes.com/services/xml/rss/nyt/HomePage.xml'):
    d = feedparser.parse(feed_url)
    return [entry.title for entry in d.entries[:10]]

# Draw screen
def draw_screen(lines, index):
    image = Image.new('1', (epd.height, epd.width), 255)
    draw = ImageDraw.Draw(image)

    y = 0
    for i in range(index, min(index + 5, len(lines))):
        draw.text((0, y), f"{i+1}. {lines[i]}", font=FONT, fill=0)
        y += 15

    # epd.display(epd.getbuffer(image))
    epd.display(epd.getbuffer(image), epd.getbuffer(image))
# Main loop
try:
    headlines = get_news()
    current_index = 0
    draw_screen(headlines, current_index)

    while True:
        if GPIO.input(BUTTONS[0]) == GPIO.LOW:  # KEY1 - Scroll up
            current_index = max(0, current_index - 1)
            draw_screen(headlines, current_index)
            time.sleep(0.3)

        if GPIO.input(BUTTONS[1]) == GPIO.LOW:  # KEY2 - Scroll down
            current_index = min(len(headlines) - 5, current_index + 1)
            draw_screen(headlines, current_index)
            time.sleep(0.3)

        if GPIO.input(BUTTONS[2]) == GPIO.LOW:  # KEY3 - Refresh feed
            headlines = get_news()
            current_index = 0
            draw_screen(headlines, current_index)
            time.sleep(0.3)

        if GPIO.input(BUTTONS[3]) == GPIO.LOW:  # KEY4 - Quit app
            epd.sleep()
            GPIO.cleanup()
            break

        time.sleep(0.1)

except KeyboardInterrupt:
    epd.sleep()
    GPIO.cleanup()
