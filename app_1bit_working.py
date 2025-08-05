#!/usr/bin/env /home/pi/e-Paper/RaspberryPi_JetsonNano/python/examples/testenv/bin/python
import os
import sys
import time
import logging
from flask import Flask, jsonify, request, render_template
from datetime import datetime

# Configure enhanced logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('/home/pi/eink_os/flask.log')
    ]
)
logger = logging.getLogger(__name__)
logger.info('Starting E-Paper Flask App - 1-bit B&W Mode')

# Set up paths
epaper_root = '/home/pi/e-Paper/RaspberryPi_JetsonNano/python'
libdir = os.path.join(epaper_root, 'lib')
examplesdir = os.path.join(epaper_root, 'examples')
picdir = os.path.join(epaper_root, 'pic')

if os.path.exists(libdir):
    sys.path.insert(0, libdir)
if os.path.exists(examplesdir):
    sys.path.insert(0, examplesdir)

# Import e-Paper library (1-bit black and white)
from waveshare_epd import epd2in7_V2
from PIL import Image, ImageDraw, ImageFont

# Initialize Flask app
app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False

# Global variable for EPD
epd = None

def init_display():
    global epd
    try:
        if epd is None:
            epd = epd2in7_V2.EPD()
        logger.info("Initializing display...")
        epd.init()
        logger.info("Display initialized successfully")
        return True
    except Exception as e:
        logger.error(f'Failed to initialize display: {e}')
        return False

def cleanup_display():
    global epd
    try:
        if epd:
            logger.info("Putting display to sleep...")
            epd.sleep()
            logger.info("Display sleep completed")
    except Exception as e:
        logger.error(f'Error during cleanup: {e}')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/clear')
def clear_display():
    logger.info("Clear display requested")
    try:
        init_display()
        logger.info("Executing epd.Clear()...")
        epd.Clear()
        logger.info("Clear operation completed")
        cleanup_display()
        return jsonify({'status': 'success', 'message': 'Display cleared'})
    except Exception as e:
        logger.error(f"Clear display error: {e}")
        return jsonify({'status': 'error', 'message': str(e)})

@app.route('/test')
def test_pattern():
    logger.info("Test pattern requested")
    try:
        init_display()
        
        # Create 1-bit black and white image
        logger.info("Creating 1-bit image...")
        image = Image.new('1', (epd.width, epd.height), 1)  # 1-bit mode, 1=white background
        draw = ImageDraw.Draw(image)
        
        # Draw test pattern with black shapes (0=black, 1=white)
        logger.info("Drawing test pattern...")
        draw.rectangle((10, 10, 60, 60), fill=0)     # Black square
        draw.rectangle((70, 10, 120, 60), fill=0)    # Black square
        draw.rectangle((130, 10, 180, 60), fill=0)   # Black square
        draw.rectangle((190, 10, 240, 60), fill=0)   # Black square
        
        draw.line((10, 80, 240, 80), fill=0, width=3)  # Black line
        draw.text((10, 100), 'Test Pattern - 1-bit B&W', fill=0)
        
        # Use 1-bit display function (not 4-bit grayscale)
        logger.info("Displaying image with epd.display()...")
        epd.display(epd.getbuffer(image))
        logger.info("Display operation completed")
        cleanup_display()
        return jsonify({'status': 'success', 'message': 'Test pattern displayed'})
    except Exception as e:
        logger.error(f"Test pattern error: {e}")
        return jsonify({'status': 'error', 'message': str(e)})

@app.route('/hello')
def hello_world():
    logger.info("Hello world requested")
    try:
        init_display()
        
        logger.info("Creating 1-bit image for hello world...")
        image = Image.new('1', (epd.width, epd.height), 1)  # 1-bit mode
        draw = ImageDraw.Draw(image)
        
        try:
            font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 24)
            logger.info("Loaded TrueType font")
        except:
            font = ImageFont.load_default()
            logger.info("Using default font")
        
        logger.info("Drawing hello world text...")
        draw.text((10, 10), 'Hello World!', font=font, fill=0)
        draw.text((10, 50), 'E-Paper Display', font=font, fill=0)
        draw.text((10, 90), '1-bit Black & White', font=font, fill=0)
        
        logger.info("Displaying hello world image...")
        epd.display(epd.getbuffer(image))
        logger.info("Hello world display completed")
        cleanup_display()
        return jsonify({'status': 'success', 'message': 'Hello World displayed'})
    except Exception as e:
        logger.error(f"Hello world error: {e}")
        return jsonify({'status': 'error', 'message': str(e)})

@app.route('/time')
def display_time():
    logger.info("Time display requested")
    try:
        init_display()
        
        logger.info("Creating 1-bit image for time...")
        image = Image.new('1', (epd.width, epd.height), 1)
        draw = ImageDraw.Draw(image)
        
        try:
            font_large = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 36)
            font_small = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 18)
            logger.info("Loaded TrueType fonts")
        except:
            font_large = ImageFont.load_default()
            font_small = ImageFont.load_default()
            logger.info("Using default fonts")
        
        current_time = datetime.now()
        time_str = current_time.strftime('%H:%M:%S')
        date_str = current_time.strftime('%Y-%m-%d')
        
        logger.info(f"Drawing time: {time_str} {date_str}")
        draw.text((20, 30), time_str, font=font_large, fill=0)
        draw.text((30, 80), date_str, font=font_small, fill=0)
        
        logger.info("Displaying time image...")
        epd.display(epd.getbuffer(image))
        logger.info("Time display completed")
        cleanup_display()
        return jsonify({'status': 'success', 'message': 'Time displayed'})
    except Exception as e:
        logger.error(f"Time display error: {e}")
        return jsonify({'status': 'error', 'message': str(e)})

@app.route('/text', methods=['POST'])
def display_text():
    logger.info("Custom text display requested")
    try:
        init_display()
        
        text = request.json.get('text', 'No text provided')
        logger.info(f"Displaying custom text: {text[:50]}...")
        
        image = Image.new('1', (epd.width, epd.height), 1)
        draw = ImageDraw.Draw(image)
        
        try:
            font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 18)
        except:
            font = ImageFont.load_default()
        
        # Simple text wrapping
        words = text.split(' ')
        lines = []
        current_line = ''
        
        for word in words:
            test_line = current_line + ' ' + word if current_line else word
            bbox = draw.textbbox((0, 0), test_line, font=font)
            if bbox[2] > epd.width - 20:
                if current_line:
                    lines.append(current_line)
                    current_line = word
                else:
                    lines.append(word)
            else:
                current_line = test_line
        
        if current_line:
            lines.append(current_line)
        
        # Draw lines
        y = 10
        for line in lines[:8]:  # Max 8 lines
            draw.text((10, y), line, font=font, fill=0)
            y += 25
        
        logger.info("Displaying custom text image...")
        epd.display(epd.getbuffer(image))
        logger.info("Custom text display completed")
        cleanup_display()
        return jsonify({'status': 'success', 'message': f'Displayed: {text[:50]}...' if len(text) > 50 else f'Displayed: {text}'})
    except Exception as e:
        logger.error(f"Custom text error: {e}")
        return jsonify({'status': 'error', 'message': str(e)})

@app.route('/sleep')
def sleep_display():
    logger.info("Sleep display requested")
    try:
        cleanup_display()
        return jsonify({'status': 'success', 'message': 'Display sleeping'})
    except Exception as e:
        logger.error(f"Sleep error: {e}")
        return jsonify({'status': 'error', 'message': str(e)})

@app.route('/wake')
def wake_display():
    logger.info("Wake display requested")
    try:
        init_display()
        return jsonify({'status': 'success', 'message': 'Display awake'})
    except Exception as e:
        logger.error(f"Wake error: {e}")
        return jsonify({'status': 'error', 'message': str(e)})

@app.route('/quiz/start')
def start_quiz():
    logger.info("Harry Potter quiz requested")
    try:
        # Import quiz module
        os.chdir(examplesdir)
        import helper_quiz as hq
        
        # Initialize and start quiz
        hpq = hq.quizGame()
        hpq.topic = 'Harry Potter'
        hpq.question_count = 4
        hpq.difficulty = 'medium'
        
        # Generate and show intro image
        topic = 'Harry Potter magical castle with wizards'
        imagepath = hpq.generate_4bit_image(topic)
        hpq.display_image_4bit(imagepath)
        
        return jsonify({'status': 'success', 'message': 'Quiz started'})
    except Exception as e:
        logger.error(f"Quiz error: {e}")
        return jsonify({'status': 'error', 'message': str(e)})

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    try:
        logger.info("Starting Flask server on 0.0.0.0:5000")
        app.run(host='0.0.0.0', port=5000, debug=False)
    except KeyboardInterrupt:
        logger.info('Shutting down...')
        cleanup_display()
        if epd:
            epd2in7_V2.epdconfig.module_exit(cleanup=True)