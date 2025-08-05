#\!/usr/bin/env python3
import os
import sys
import subprocess

# Path to the virtual environment python
venv_python = "/home/pi/e-Paper/RaspberryPi_JetsonNano/python/examples/testenv/bin/python"

# Path to the portable script
script_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "harrypotter_quiz_portable.py")

# Run the script with the virtual environment Python
subprocess.run([venv_python, script_path])
