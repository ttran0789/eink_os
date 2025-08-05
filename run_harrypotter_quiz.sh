#\!/bin/bash

# Activate the virtual environment
source /home/pi/e-Paper/RaspberryPi_JetsonNano/python/examples/testenv/bin/activate

# Set up environment
export PYTHONPATH="/home/pi/e-Paper/RaspberryPi_JetsonNano/python/lib:/home/pi/e-Paper/RaspberryPi_JetsonNano/python/examples:$PYTHONPATH"

# Change to examples directory (for relative file access)
cd /home/pi/e-Paper/RaspberryPi_JetsonNano/python/examples

# Run the quiz
python /home/pi/eink_os/harrypotter_quiz.py

# Deactivate virtual environment
deactivate
