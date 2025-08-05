#\!/usr/bin/env python3
import os
import sys

# Add the waveshare library path
sys.path.insert(0, '/home/pi/e-Paper/RaspberryPi_JetsonNano/python/lib')

# Add the examples directory for helper modules
sys.path.insert(0, '/home/pi/e-Paper/RaspberryPi_JetsonNano/python/examples')

# Change working directory to examples folder to ensure relative paths work
os.chdir('/home/pi/e-Paper/RaspberryPi_JetsonNano/python/examples')

# Now import and run the actual quiz
from harrypotter_quiz import *

# The script will run the __main__ block from the imported module
