#\!/usr/bin/env /home/pi/e-Paper/RaspberryPi_JetsonNano/python/examples/testenv/bin/python
import os
import sys
import time
import logging
from flask import Flask, jsonify, request, render_template_string
from datetime import datetime

# Set up paths
epaper_root = '/home/pi/e-Paper/RaspberryPi_JetsonNano/python'
libdir = os.path.join(epaper_root, 'lib')
examplesdir = os.path.join(epaper_root, 'examples')
picdir = os.path.join(epaper_root, 'pic')

if os.path.exists(libdir):
    sys.path.insert(0, libdir)
if os.path.exists(examplesdir):
    sys.path.insert(0, examplesdir)

# Import e-Paper library
from waveshare_epd import epd2in7b_V2
from PIL import Image, ImageDraw, ImageFont

# Initialize Flask app
app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False

# Global variable for EPD
epd = None

def init_display():
    global epd
    try:
        epd = epd2in7b_V2.EPD()
        epd.init()
        return True
    except Exception as e:
        logging.error(f'Failed to initialize display: {e}')
        return False

@app.route('/')
def index():
    return '<h1>E-Paper Display API</h1><p>Use /clear, /test, /hello, /time, /sleep, /wake</p>'

@app.route('/clear')
def clear_display():
    try:
        if not epd:
            init_display()
        epd.Clear()
        return jsonify({'status': 'success', 'message': 'Display cleared'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

@app.route('/test')
def test_pattern():
    try:
        if not epd:
            init_display()
            
        # Create images
        blackimage = Image.new('1', (epd.height, epd.width), 255)
        redimage = Image.new('1', (epd.height, epd.width), 255)
        
        draw_black = ImageDraw.Draw(blackimage)
        draw_red = ImageDraw.Draw(redimage)
        
        # Draw test pattern
        draw_black.rectangle((10, 10, 110, 110), outline=0)
        draw_red.rectangle((120, 10, 220, 110), fill=0)
        draw_black.line((10, 60, 220, 60), fill=0)
        
        epd.display(epd.getbuffer(blackimage), epd.getbuffer(redimage))
        return jsonify({'status': 'success', 'message': 'Test pattern displayed'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

@app.route('/hello')
def hello_world():
    try:
        if not epd:
            init_display()
            
        blackimage = Image.new('1', (epd.height, epd.width), 255)
        redimage = Image.new('1', (epd.height, epd.width), 255)
        
        draw = ImageDraw.Draw(blackimage)
        font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 24)
        
        draw.text((10, 10), 'Hello World\!', font=font, fill=0)
        draw.text((10, 50), 'E-Paper Display', font=font, fill=0)
        
        epd.display(epd.getbuffer(blackimage), epd.getbuffer(redimage))
        return jsonify({'status': 'success', 'message': 'Hello World displayed'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

@app.route('/time')
def display_time():
    try:
        if not epd:
            init_display()
            
        blackimage = Image.new('1', (epd.height, epd.width), 255)
        redimage = Image.new('1', (epd.height, epd.width), 255)
        
        draw = ImageDraw.Draw(blackimage)
        font_large = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 36)
        font_small = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 18)
        
        current_time = datetime.now()
        time_str = current_time.strftime('%H:%M:%S')
        date_str = current_time.strftime('%Y-%m-%d')
        
        draw.text((50, 30), time_str, font=font_large, fill=0)
        draw.text((70, 80), date_str, font=font_small, fill=0)
        
        epd.display(epd.getbuffer(blackimage), epd.getbuffer(redimage))
        return jsonify({'status': 'success', 'message': 'Time displayed'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

@app.route('/sleep')
def sleep_display():
    try:
        if not epd:
            init_display()
        epd.sleep()
        return jsonify({'status': 'success', 'message': 'Display sleeping'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

@app.route('/wake')
def wake_display():
    try:
        init_display()
        return jsonify({'status': 'success', 'message': 'Display awake'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    init_display()
    app.run(host='0.0.0.0', port=5000, debug=True)
