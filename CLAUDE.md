# E-Paper Display Control System

## Project Overview
This project creates a Flask web application to remotely control a Waveshare 2.7" 4-bit grayscale e-Paper display connected to a Raspberry Pi. The system allows users to display text, images, patterns, and run interactive applications like a Harry Potter quiz through a web interface.

## Hardware Setup
- **Device**: Raspberry Pi 3B
- **Display**: Waveshare 2.7" 4-bit grayscale e-Paper display (epd2in7_V2)
- **Network**: WiFi connected at 192.168.0.9
- **GPIO**: Uses GPIO pins for SPI communication with the display

## Project Structure

### Raspberry Pi Directory Structure
```
/home/pi/eink_os/
├── app.py                          # Basic Flask app
├── app_enhanced.py                 # Enhanced Flask app with web UI
├── app_safe.py                     # Safe version with error handling
├── harrypotter_quiz.py             # Original quiz wrapper
├── harrypotter_quiz_portable.py    # Portable version with dynamic paths
├── harrypotter_quiz_standalone.py  # Standalone version with venv
├── hp_quiz_launcher.py             # Launcher script
├── start_server.sh                 # Server startup script
├── flask.log                       # Flask application logs
└── templates/
    ├── index.html                  # Main web interface
    └── debug.html                  # Debug interface

/home/pi/e-Paper/RaspberryPi_JetsonNano/python/
├── lib/                            # Waveshare EPD library
│   └── waveshare_epd/
├── examples/                       # Original examples and dependencies
│   ├── harrypotter_quiz.py         # Original Harry Potter quiz
│   ├── helper_quiz.py               # Quiz helper functions
│   ├── image_generator.py           # AI image generation
│   ├── testenv/                     # Virtual environment
│   └── .env                        # Environment variables (OpenAI key)
└── pic/                            # Image assets
```

## Key Components

### 1. Flask Web Application (`app_enhanced.py`)
- **Framework**: Flask web server
- **Port**: 5000 (accessible at http://192.168.0.9:5000)
- **Features**:
  - Web-based control interface
  - Real-time status updates
  - Error handling and logging
  - RESTful API endpoints

### 2. Display Functions
- **Clear Display**: `/clear` - Clears the e-Paper screen
- **Test Pattern**: `/test` - Displays geometric shapes and lines
- **Hello World**: `/hello` - Shows greeting text
- **Current Time**: `/time` - Displays current date and time
- **Custom Text**: `/text` (POST) - Shows user-provided text with word wrapping
- **Sleep/Wake**: `/sleep`, `/wake` - Power management
- **Harry Potter Quiz**: `/quiz/start` - Launches interactive quiz with AI-generated images

### 3. Path Resolution System
The project uses dynamic path resolution to work from any location:
```python
epaper_root = '/home/pi/e-Paper/RaspberryPi_JetsonNano/python'
libdir = os.path.join(epaper_root, 'lib')
examplesdir = os.path.join(epaper_root, 'examples')
```

### 4. Virtual Environment Integration
- **Location**: `/home/pi/e-Paper/RaspberryPi_JetsonNano/python/examples/testenv/`
- **Dependencies**: Flask, OpenAI, PIL, python-dotenv
- **Activation**: Handled automatically by shebang or startup scripts

## API Endpoints

### GET Endpoints
- `GET /` - Main web interface
- `GET /clear` - Clear display
- `GET /test` - Show test pattern
- `GET /hello` - Display "Hello World"
- `GET /time` - Show current time
- `GET /sleep` - Put display to sleep
- `GET /wake` - Wake display
- `GET /quiz/start` - Start Harry Potter quiz
- `GET /debug` - Debug interface

### POST Endpoints
- `POST /text` - Display custom text
  ```json
  {
    "text": "Your custom message here"
  }
  ```

## Usage Instructions

### Starting the Server
```bash
# SSH into Raspberry Pi
ssh -i "C:\Users\tuan\.ssh\id_rsa_pi3b" pi@192.168.0.9

# Navigate to project directory
cd /home/pi/eink_os

# Start server
./start_server.sh

# Or start manually
/home/pi/e-Paper/RaspberryPi_JetsonNano/python/examples/testenv/bin/python app_enhanced.py
```

### Accessing the Web Interface
1. Open web browser
2. Navigate to: `http://192.168.0.9:5000`
3. Use buttons to control the display
4. Enter custom text in the input field

### Monitoring Logs
```bash
# View logs in real-time
tail -f /home/pi/eink_os/flask.log

# View recent logs
tail -20 /home/pi/eink_os/flask.log
```

### Running Harry Potter Quiz Standalone
```bash
# From anywhere on the Pi
/home/pi/eink_os/harrypotter_quiz_standalone.py

# Or using launcher
/home/pi/eink_os/hp_quiz_launcher.py
```

## Technical Details

### Display Specifications
- **Model**: Waveshare 2.7" e-Paper Display (epd2in7_V2)
- **Resolution**: 264x176 pixels
- **Colors**: 4-bit grayscale (16 levels of gray)
- **Interface**: SPI communication via GPIO
- **Refresh Time**: 4-15 seconds for full refresh
- **Power Consumption**: Very low (μA in sleep mode)
- **Viewing Angle**: Nearly 180° (paper-like)
- **Update Mechanism**: Electrophoretic display technology

### Critical Implementation Notes

**Display Driver Functions:**
- **Standard Display**: `epd.display(epd.getbuffer(image))` - For 1-bit images
- **4-bit Grayscale**: `epd.display_4Gray(epd.getbuffer_4Gray(image))` - For grayscale images
- **Clear Function**: `epd.Clear()` - Clears to white/blank
- **Initialization**: `epd.init()` - Must call before operations
- **Sleep Mode**: `epd.sleep()` - Low power mode

**Image Creation:**
```python
# For grayscale images
image = Image.new('L', (epd.width, epd.height), 255)  # L=grayscale, 255=white
draw = ImageDraw.Draw(image)
draw.rectangle((x, y, x2, y2), fill=128)  # 128 = medium gray
epd.display_4Gray(epd.getbuffer_4Gray(image))
```

**GPIO Pin Usage:**
- Uses SPI interface (MOSI, MISO, CLK, CS)
- Additional control pins for reset, data/command, busy status
- Shared with other SPI devices - avoid conflicts

### Libraries Used
- **Flask**: Web framework
- **Pillow (PIL)**: Image processing
- **waveshare_epd**: E-Paper display driver
- **OpenAI**: AI image generation (for quiz)
- **gpiozero**: GPIO control

### Error Handling
- GPIO busy detection
- Display initialization failures
- Network connectivity issues
- Font loading fallbacks
- Text wrapping for long messages

## Troubleshooting

### Common Issues

1. **GPIO Busy Error**
   ```
   lgpio.error: 'GPIO busy'
   ```
   - **Solution**: Kill existing processes using GPIO or reboot Pi
   - **Cause**: Multiple processes trying to use the same GPIO pins
   - **Check**: `ps aux | grep python` to find conflicting processes

2. **Display Not Responding**
   - Check GPIO connections
   - Verify SPI is enabled: `sudo raspi-config`
   - Test with original Waveshare examples

3. **Web Interface Not Accessible**
   - Verify server is running: `ss -tlnp | grep :5000`
   - Check network connectivity
   - Try SSH tunnel: `ssh -L 8080:localhost:5000 pi@192.168.0.9`

4. **Buttons Appear Not Working**
   - **IMPORTANT**: E-Paper displays are VERY SLOW (4-15 seconds to update)
   - Wait for response - the display shows "e-Paper busy" during updates
   - Check browser console for JavaScript errors
   - Verify API endpoints work: `curl http://192.168.0.9:5000/test`
   - Clear screen may not be visually obvious (blank to blank)

5. **Cron Job Conflicts**
   - Multiple services starting at boot can cause GPIO conflicts
   - Check crontab: `crontab -l | grep @reboot`
   - Disable conflicting services if needed

### Important Display Behavior

**E-Paper Display Characteristics:**
- **Update Time**: 4-15 seconds for full refresh
- **Busy State**: Display shows "busy" status during updates
- **Grayscale Levels**: 16 levels (0=black, 255=white)  
- **Power Management**: Automatically goes to sleep after operations
- **Refresh Type**: Full screen refresh (no partial updates in current implementation)

**API Response vs Visual Update:**
- API returns `{"status":"success"}` immediately
- Physical display update happens asynchronously
- Wait 5-15 seconds to see visual changes on screen

### Log Analysis
```bash
# Check for errors
grep -i error /home/pi/eink_os/flask.log

# Monitor requests
grep -i "GET\|POST" /home/pi/eink_os/flask.log

# Check initialization
grep -i "init" /home/pi/eink_os/flask.log
```

## Development Notes

### Adding New Display Functions
1. Create new route in `app_enhanced.py`:
```python
@app.route('/new_function')
def new_function():
    try:
        # Your display code here
        return jsonify({'status': 'success', 'message': 'Function executed'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})
```

2. Add button to `templates/index.html`:
```html
<button class="button" onclick="callAPI('/new_function')">New Function</button>
```

### Image Processing Tips
- Use PIL for image manipulation
- Convert to 4-bit grayscale (16 levels) for optimal display
- Resize images to fit display: 264x176 or 176x264
- Use `epd.getbuffer()` to prepare for display
- The quiz uses `generate_4bit_image()` for AI-generated grayscale images

### Performance Considerations
- E-Paper displays are slow (~15 second refresh)
- Avoid frequent updates
- Use partial refresh for simple changes (if supported)
- Cache commonly used images

## Future Enhancements

### Planned Features
- [ ] Image upload functionality
- [ ] Multiple quiz topics
- [ ] Weather display integration
- [ ] Calendar/schedule display
- [ ] Drawing/sketching interface
- [ ] Multiple display support
- [ ] Mobile-responsive design improvements

### Security Considerations
- Add authentication for web interface
- Implement HTTPS
- Rate limiting for API endpoints
- Input validation for custom text
- Secure file upload handling

## Resources

### Documentation
- [Waveshare E-Paper HAT Manual](https://www.waveshare.com/wiki/2.7inch_e-Paper_HAT)
- [Flask Documentation](https://flask.palletsprojects.com/)
- [Raspberry Pi GPIO Pinout](https://pinout.xyz/)

### Related Files
- **SSH Key**: `C:\Users\tuan\.ssh\id_rsa_pi3b`
- **Original Examples**: `/home/pi/e-Paper/RaspberryPi_JetsonNano/python/examples/`
- **Waveshare Library**: `/home/pi/e-Paper/RaspberryPi_JetsonNano/python/lib/`

## Commands Reference

### Server Management
```bash
# Start server (current working version)
cd /home/pi/eink_os && /home/pi/e-Paper/RaspberryPi_JetsonNano/python/examples/testenv/bin/python app_4bit.py > flask.log 2>&1 &

# Stop server
pkill -f app_4bit.py

# Check server status
ss -tlnp | grep :5000
ps aux | grep app_4bit

# View logs
tail -f /home/pi/eink_os/flask.log

# Test server endpoints
curl http://localhost:5000/clear
curl http://localhost:5000/test
curl http://localhost:5000/hello
```

### GPIO and Process Management
```bash
# Check for GPIO conflicts
ps aux | grep python | grep -v grep

# Kill all Python processes (use with caution)
pkill python

# Check cron jobs
crontab -l | grep @reboot

# Test original Waveshare example
cd /home/pi/e-Paper/RaspberryPi_JetsonNano/python/examples
/home/pi/e-Paper/RaspberryPi_JetsonNano/python/examples/testenv/bin/python epd_2in7_V2_test.py
```

### Display Testing
```bash
# Test API endpoints
curl http://192.168.0.9:5000/clear
curl http://192.168.0.9:5000/test
curl http://192.168.0.9:5000/hello

# Test with custom text
curl -X POST -H "Content-Type: application/json" -d '{"text":"Hello from curl!"}' http://192.168.0.9:5000/text
```

### System Information
```bash
# Check Pi network info
ip addr show wlan0

# Check GPIO usage
sudo lsof /dev/gpiomem

# Check Python processes
ps aux | grep python

# Check system logs
journalctl -u ssh
```