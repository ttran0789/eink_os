# E-Paper Display Control System

A Flask web application for remotely controlling a Waveshare 2.7" 4-bit grayscale e-Paper display connected to a Raspberry Pi. Control your e-Paper display through a web interface from any device on your network.

## 🖥️ Features

- **Web-based Control Interface** - Clean, responsive web UI with buttons and forms
- **Multiple Display Functions** - Clear screen, show text, display patterns, show current time
- **Custom Text Display** - Enter any text with automatic word wrapping
- **Harry Potter Quiz** - Interactive quiz with AI-generated grayscale images
- **Real-time Status Updates** - Live feedback on display operations
- **Multiple App Versions** - Different Flask apps for various use cases
- **Comprehensive Logging** - Detailed logs for debugging and monitoring
- **Startup Scripts** - Easy server management and auto-start capabilities

## 🛠️ Hardware Requirements

- **Raspberry Pi** (tested on Pi 3B)
- **Waveshare 2.7" e-Paper Display** (epd2in7_V2)
- **GPIO Connection** via SPI interface
- **WiFi Connection** for remote access

## 📋 Display Specifications

- **Model**: Waveshare 2.7" e-Paper Display (epd2in7_V2)
- **Resolution**: 264x176 pixels
- **Colors**: 4-bit grayscale (16 levels)
- **Refresh Time**: 4-15 seconds
- **Interface**: SPI via GPIO
- **Power**: Ultra-low consumption (μA in sleep mode)

## 🚀 Quick Start

### 1. Clone Repository
```bash
git clone https://github.com/ttran0789/eink_os.git
cd eink_os
```

### 2. Hardware Setup
Connect your Waveshare 2.7" e-Paper display to your Raspberry Pi via SPI pins. Ensure SPI is enabled:
```bash
sudo raspi-config
# Navigate to Interface Options > SPI > Enable
```

### 3. Install Dependencies
```bash
# Install system dependencies
sudo apt update
sudo apt install python3-pip python3-venv

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install Python packages
pip install flask pillow python-dotenv openai
```

### 4. Configure Environment
```bash
# Copy environment template
cp examples/.env.example examples/.env

# Edit with your OpenAI API key (for quiz feature)
nano examples/.env
```

### 5. Start the Server
```bash
# Make scripts executable
chmod +x start_server.sh

# Start the Flask application
./start_server.sh

# Or start manually
python app_4bit.py
```

### 6. Access Web Interface
Open your browser and navigate to:
```
http://your-pi-ip:5000
```

## 🎮 Usage

### Web Interface
The main interface provides buttons for common operations:
- **Clear Display** - Blank the screen
- **Test Pattern** - Show geometric shapes and lines
- **Hello World** - Display greeting message
- **Show Time** - Current date and time
- **Custom Text** - Enter your own message
- **Harry Potter Quiz** - Start interactive quiz
- **Sleep/Wake** - Power management

### API Endpoints

#### GET Endpoints
```http
GET /           # Main web interface
GET /clear      # Clear display
GET /test       # Show test pattern
GET /hello      # Display "Hello World"
GET /time       # Show current time
GET /sleep      # Put display to sleep
GET /wake       # Wake display
GET /quiz/start # Start Harry Potter quiz
```

#### POST Endpoints
```http
POST /text      # Display custom text
Content-Type: application/json
{
  "text": "Your custom message here"
}
```

### Command Line Usage
```bash
# Test display directly
python examples/epd_2in7_V2_test.py

# Run quiz standalone
python harrypotter_quiz_standalone.py

# Check server status
curl http://localhost:5000/clear
```

## 📁 Project Structure

```
eink_os/
├── app_4bit.py                    # Main Flask application (4-bit grayscale)
├── app_enhanced.py               # Enhanced version with full web UI
├── app_safe.py                   # Version with extensive error handling
├── templates/                    # HTML templates
│   ├── index.html               # Main web interface
│   └── debug.html               # Debug interface
├── lib/                         # Waveshare EPD library
│   └── waveshare_epd/          # Display drivers
├── examples/                    # Example scripts and components
│   ├── harrypotter_quiz.py     # Interactive quiz
│   ├── helper_quiz.py          # Quiz helper functions
│   ├── image_generator.py      # AI image generation
│   └── .env.example           # Environment template
├── pic/                        # Image assets
├── scripts/                    # Startup and utility scripts
└── CLAUDE.md                   # Detailed project documentation
```

## ⚙️ Configuration

### Environment Variables
Create `examples/.env` with:
```bash
OPENAI_KEY=your_openai_api_key_here
```

### Network Access
The Flask server runs on port 5000. To access from other devices:
1. Find your Pi's IP address: `ip addr show wlan0`
2. Ensure port 5000 is accessible (no firewall blocking)
3. Access via `http://PI_IP_ADDRESS:5000`

### Auto-start on Boot
```bash
# Add to crontab
crontab -e

# Add this line:
@reboot cd /path/to/eink_os && ./start_server.sh
```

## 🔧 Troubleshooting

### Common Issues

**GPIO Busy Error**
```bash
# Check for conflicting processes
ps aux | grep python
# Kill conflicting processes or reboot
sudo reboot
```

**Display Not Responding**
- Check GPIO connections
- Verify SPI is enabled: `sudo raspi-config`
- Test with original examples

**Web Interface Slow**
- **Normal behavior** - e-Paper displays take 4-15 seconds to update
- Wait for "e-Paper busy" status to clear
- Don't click buttons multiple times rapidly

**Quiz Images Not Generating**
- Ensure OpenAI API key is set in `examples/.env`
- Check internet connectivity
- Verify OpenAI account has credits

### Logs
Monitor application logs:
```bash
# View real-time logs
tail -f flask.log

# Check for errors
grep -i error flask.log
```

## 🎯 API Examples

### Using curl
```bash
# Clear display
curl http://192.168.0.9:5000/clear

# Show custom text
curl -X POST -H "Content-Type: application/json" \
     -d '{"text":"Hello from API!"}' \
     http://192.168.0.9:5000/text

# Get current time display
curl http://192.168.0.9:5000/time
```

### Using Python requests
```python
import requests

# Clear display
response = requests.get('http://192.168.0.9:5000/clear')
print(response.json())

# Send custom text
data = {'text': 'Hello from Python!'}
response = requests.post('http://192.168.0.9:5000/text', json=data)
print(response.json())
```

## 🎨 Customization

### Adding New Display Functions
1. Add route to Flask app:
```python
@app.route('/custom')
def custom_display():
    try:
        # Your display code here
        epd = epd2in7_V2.EPD()
        epd.init()
        
        # Create and display image
        image = Image.new('L', (epd.width, epd.height), 255)
        draw = ImageDraw.Draw(image)
        draw.text((10, 10), "Custom Function", fill=0)
        
        epd.display_4Gray(epd.getbuffer_4Gray(image))
        epd.sleep()
        
        return jsonify({'status': 'success'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})
```

2. Add button to HTML template:
```html
<button class="button" onclick="callAPI('/custom')">Custom Function</button>
```

### Image Processing Tips
- Use PIL/Pillow for image manipulation
- Convert images to 4-bit grayscale for optimal display
- Resize to display dimensions: 264x176 pixels
- Use dithering for better grayscale representation

## 🔒 Security

- API keys are excluded from repository via `.gitignore`
- Use environment variables for sensitive configuration
- Consider adding authentication for production use
- Implement HTTPS for secure remote access

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes and test thoroughly
4. Commit with descriptive messages
5. Push and create a Pull Request

## 📄 License

This project is open source. See individual component licenses for details.

## 🙏 Acknowledgments

- [Waveshare](https://www.waveshare.com/) for e-Paper display drivers
- [Flask](https://flask.palletsprojects.com/) web framework
- [OpenAI](https://openai.com/) for AI image generation
- Raspberry Pi Foundation for the amazing hardware platform

## 📞 Support

- Check [CLAUDE.md](CLAUDE.md) for detailed technical documentation
- Review logs in `flask.log` for debugging
- Test with original Waveshare examples if display issues occur
- Ensure proper GPIO connections and SPI configuration

---

**Made with ❤️ for e-Paper display enthusiasts**