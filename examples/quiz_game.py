import sys
import time
from PIL import Image, ImageDraw, ImageFont
from gpiozero import Button
sys.path.append('../lib')  # Path to Waveshare library
from waveshare_epd import epd2in7b_V2

# Setup
epd = epd2in7b_V2.EPD()
epd.init()
epd.Clear()

FONT = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 16)
WIDTH, HEIGHT = epd.width, epd.height

# Buttons
btn1 = Button(5)   # KEY1
btn2 = Button(6)   # KEY2
btn3 = Button(13)  # KEY3
btn4 = Button(19)  # KEY4

# Questions format: (question, [options], correct_index)
questions = [
    ("What’s the capital of France?", ["Berlin", "London", "Paris", "Rome"], 2),
    ("2 + 2 equals?", ["3", "4", "5", "22"], 1),
    ("Which planet is red?", ["Earth", "Venus", "Mars", "Jupiter"], 2),
]

score = 0
q_index = 0

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

while q_index < len(questions):
    q, options, correct = questions[q_index]
    show_text([f"Q{q_index+1}: {q}"] + [f"{i+1}. {opt}" for i, opt in enumerate(options)])
    choice = wait_for_button()
    
    if choice == correct:
        score += 1
        show_text(["✅ Correct!", "", "Next question..."])
    else:
        show_text(["❌ Incorrect!", f"Correct was: {options[correct]}", "", "Next question..."])
    time.sleep(2)
    q_index += 1

# Final score
show_text([f"🎉 Quiz Complete!", f"Your score: {score}/{len(questions)}"])
time.sleep(10)
epd.sleep()
