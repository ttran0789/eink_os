#!/usr/bin/env /home/pi/e-Paper/RaspberryPi_JetsonNano/python/examples/testenv/bin/python
import os
import sys
import time
import logging
import glob
import json
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
images_dir = '/home/pi/rpi-screen/images'  # AI generated images directory
metadata_file = '/home/pi/rpi-screen/image_metadata.json'  # Image descriptions/prompts

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

def init_display_4gray():
    """Initialize display for 4-bit grayscale mode (for pre-made bitmaps)"""
    global epd
    try:
        if epd is None:
            epd = epd2in7_V2.EPD()
        logger.info("Initializing display for 4-bit grayscale...")
        epd.Init_4Gray()
        logger.info("4-bit grayscale display initialized successfully")
        return True
    except Exception as e:
        logger.error(f'Failed to initialize 4-bit display: {e}')
        return False

def display_image_4bit(filepath):
    """Display a 4-level grayscale bitmap image (works with pre-made bitmaps)"""
    logger.info(f"Displaying 4-bit image: {filepath}")
    try:
        init_display_4gray()
        
        # Load and process image
        img = Image.open(filepath).convert('L')  # Convert to grayscale
        img = img.resize((epd.height, epd.width))  # Note: height x width for landscape
        
        # Map to 4 grayscale levels: 0, 85, 170, 255 (Harry Potter quiz technique)
        logger.info("Applying 4-level grayscale mapping...")
        img = img.point(lambda x: 0 if x < 64 else 85 if x < 128 else 170 if x < 192 else 255, 'L')
        
        # Display using 4-bit grayscale mode
        logger.info("Displaying 4-bit grayscale image...")
        epd.display_4Gray(epd.getbuffer_4Gray(img))
        logger.info("4-bit image display completed")
        
        time.sleep(2)
        cleanup_display()
        return True
        
    except Exception as e:
        logger.error(f"Error displaying 4-bit image: {e}")
        return False

def load_image_metadata():
    """Load image metadata from JSON file"""
    try:
        if os.path.exists(metadata_file):
            with open(metadata_file, 'r') as f:
                return json.load(f)
        else:
            return {}
    except Exception as e:
        logger.error(f"Error loading metadata: {e}")
        return {}

def save_image_metadata(metadata):
    """Save image metadata to JSON file"""
    try:
        with open(metadata_file, 'w') as f:
            json.dump(metadata, f, indent=2)
        return True
    except Exception as e:
        logger.error(f"Error saving metadata: {e}")
        return False

def get_image_description(filename):
    """Get description for an image, with fallbacks"""
    metadata = load_image_metadata()
    
    # Check if we have a specific description
    if filename in metadata:
        return metadata[filename]
    
    # Generate a default description based on timestamp and type
    if 'ai_hp' in filename:
        # Extract timestamp if available
        import re
        match = re.search(r'(\d{8}_\d{6})', filename)
        if match:
            timestamp_str = match.group(1)
            try:
                # Parse timestamp: YYYYMMDD_HHMMSS
                from datetime import datetime
                timestamp = datetime.strptime(timestamp_str, '%Y%m%d_%H%M%S')
                date_str = timestamp.strftime('%B %d, %Y at %I:%M %p')
                return f"Harry Potter magical world artwork generated on {date_str}. Features Hogwarts castle, magical creatures, wizarding world elements, and enchanted landscapes."
            except:
                pass
        
        return "AI-generated Harry Potter magical world artwork featuring Hogwarts castle, magical creatures, and wizarding world elements with vibrant, enchanted landscapes."
    
    return "AI-generated artwork"

def update_image_metadata(filename, description):
    """Update description for a specific image"""
    metadata = load_image_metadata()
    metadata[filename] = description
    return save_image_metadata(metadata)

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

@app.route('/images/list')
def list_images():
    """List all available AI-generated images with descriptions"""
    logger.info("Image list requested")
    try:
        if not os.path.exists(images_dir):
            return jsonify({'status': 'error', 'message': 'Images directory not found'})
        
        # Find all resized Harry Potter images (these are display-ready)
        pattern = os.path.join(images_dir, 'ai_hp*resized*.bmp')
        image_files = glob.glob(pattern)
        
        # Sort by modification time (newest first)
        image_files.sort(key=os.path.getmtime, reverse=True)
        
        # Create image objects with metadata
        images_with_metadata = []
        for filepath in image_files[:50]:  # Limit to 50 most recent
            filename = os.path.basename(filepath)
            description = get_image_description(filename)
            
            # Get file modification time for display
            try:
                mtime = os.path.getmtime(filepath)
                from datetime import datetime
                created_date = datetime.fromtimestamp(mtime).strftime('%m/%d/%Y %I:%M %p')
            except:
                created_date = 'Unknown'
            
            images_with_metadata.append({
                'filename': filename,
                'description': description,
                'created': created_date
            })
        
        logger.info(f"Found {len(image_files)} images, returning {len(images_with_metadata)} with metadata")
        return jsonify({
            'status': 'success', 
            'message': f'Found {len(image_files)} images',
            'images': images_with_metadata,
            'total_count': len(image_files)
        })
    except Exception as e:
        logger.error(f"Error listing images: {e}")
        return jsonify({'status': 'error', 'message': str(e)})

@app.route('/images/display', methods=['POST'])
def display_selected_image():
    """Display a selected image from the gallery"""
    logger.info("Image display requested")
    try:
        data = request.json
        if not data or 'filename' not in data:
            return jsonify({'status': 'error', 'message': 'Filename required'})
        
        filename = data['filename']
        filepath = os.path.join(images_dir, filename)
        
        # Security check - ensure file exists and is in images directory
        if not os.path.exists(filepath):
            return jsonify({'status': 'error', 'message': 'Image file not found'})
        
        if not os.path.abspath(filepath).startswith(os.path.abspath(images_dir)):
            return jsonify({'status': 'error', 'message': 'Invalid file path'})
        
        # Display the image using 4-bit grayscale (works with pre-made bitmaps)
        success = display_image_4bit(filepath)
        
        if success:
            return jsonify({'status': 'success', 'message': f'Displaying image: {filename}'})
        else:
            return jsonify({'status': 'error', 'message': 'Failed to display image'})
            
    except Exception as e:
        logger.error(f"Error displaying image: {e}")
        return jsonify({'status': 'error', 'message': str(e)})

@app.route('/images/random')
def display_random_image():
    """Display a random image from the gallery"""
    logger.info("Random image requested")
    try:
        if not os.path.exists(images_dir):
            return jsonify({'status': 'error', 'message': 'Images directory not found'})
        
        # Find all resized images
        pattern = os.path.join(images_dir, 'ai_hp*resized*.bmp')
        image_files = glob.glob(pattern)
        
        if not image_files:
            return jsonify({'status': 'error', 'message': 'No images found'})
        
        # Select random image
        import random
        selected_file = random.choice(image_files)
        filename = os.path.basename(selected_file)
        
        # Display the image
        success = display_image_4bit(selected_file)
        
        if success:
            return jsonify({'status': 'success', 'message': f'Displaying random image: {filename}'})
        else:
            return jsonify({'status': 'error', 'message': 'Failed to display random image'})
            
    except Exception as e:
        logger.error(f"Error displaying random image: {e}")
        return jsonify({'status': 'error', 'message': str(e)})

@app.route('/images/update_description', methods=['POST'])
def update_image_description():
    """Update description for an image"""
    logger.info("Image description update requested")
    try:
        data = request.json
        if not data or 'filename' not in data or 'description' not in data:
            return jsonify({'status': 'error', 'message': 'Filename and description required'})
        
        filename = data['filename']
        description = data['description'].strip()
        
        if not description:
            return jsonify({'status': 'error', 'message': 'Description cannot be empty'})
        
        # Security check - ensure filename is valid
        filepath = os.path.join(images_dir, filename)
        if not os.path.exists(filepath):
            return jsonify({'status': 'error', 'message': 'Image file not found'})
        
        # Update metadata
        success = update_image_metadata(filename, description)
        
        if success:
            logger.info(f"Updated description for {filename}: {description[:50]}...")
            return jsonify({'status': 'success', 'message': f'Updated description for {filename}'})
        else:
            return jsonify({'status': 'error', 'message': 'Failed to save description'})
            
    except Exception as e:
        logger.error(f"Error updating image description: {e}")
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