#\!/bin/bash
# Wait for network to be ready
sleep 30

# Kill any existing Flask processes
pkill -f app_4bit.py

# Start Flask app with logging
cd /home/pi/eink_os
/home/pi/e-Paper/RaspberryPi_JetsonNano/python/examples/testenv/bin/python app_4bit.py > /home/pi/eink_os/flask_console.log 2>&1 &

# Log startup
echo "Tue, Aug  5, 2025  1:08:53 AM: Flask app started automatically" >> /home/pi/eink_os/startup.log
