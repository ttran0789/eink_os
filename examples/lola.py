from PIL import Image
import time
import sys
import os

# Path to the Waveshare library
sys.path.append('/home/pi/e-Paper/RaspberryPi_JetsonNano/python/lib')
from waveshare_epd import epd2in7_V2  # Use the correct driver

# Init
epd = epd2in7_V2.EPD()
epd.init()
epd.Clear()

# Load and prepare image
fp_lola_img = '/home/pi/rpi-screen/lola2.bmp'
image = Image.open(fp_lola_img).resize((epd.height, epd.width)).convert('1')

# Show the image
epd.display(epd.getbuffer(image))

# Sleep
time.sleep(2)
epd.sleep()
