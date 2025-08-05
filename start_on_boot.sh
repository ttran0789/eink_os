#\!/bin/bash
# Wait for network to be ready
sleep 30

# Change to project directory
cd /home/pi/eink_os

# Start Flask server
/home/pi/e-Paper/RaspberryPi_JetsonNano/python/examples/testenv/bin/python app_enhanced.py > flask_boot.log 2>&1 &

# Log startup
echo "Flask server started at \Mon, Aug  4, 2025 11:37:59 PM" >> /home/pi/eink_os/startup.log
