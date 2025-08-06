# E-Paper Display Control System

A comprehensive Flask web application that transforms a Raspberry Pi + Waveshare e-Paper display into a complete AI art creation and display platform. Generate custom images with OpenAI DALL-E 3, browse a gallery of 185+ AI artworks, and control your e-Paper display through an intuitive web interface.

## ✨ Features

### 🎨 AI Image Generation
- **Custom Image Creation** - Generate any image from text prompts using OpenAI DALL-E 3
- **Instant Display** - Create and display images in ~25 seconds
- **Gallery Integration** - Save generated images to browseable gallery
- **Perfect Processing** - Automatic cropping, resizing, and grayscale optimization for e-Paper

### 🖼️ Advanced Image Gallery  
- **185+ AI Artworks** - Pre-generated Harry Potter themed images + your custom creations
- **Smart Descriptions** - Each image has contextual descriptions and creation dates
- **Interactive Browsing** - Click to display any image, edit descriptions, or get random art
- **Metadata Management** - Persistent storage of prompts and descriptions

### 💻 Complete Web Interface
- **Intuitive Design** - Modern, responsive UI with real-time status updates
- **Multiple Display Modes** - Text, patterns, time display, and image gallery
- **Error Handling** - Robust validation and user-friendly error messages
- **Live Feedback** - Progress tracking for AI generation and display operations

### 🔧 Technical Excellence
- **Hybrid Display System** - 1-bit B&W for text + 4-bit grayscale for images
- **Comprehensive Logging** - Detailed logs for debugging and monitoring
- **RESTful API** - Complete endpoint coverage for integration and automation
- **Optimized Performance** - Fast image processing and efficient e-Paper refreshing

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

# Edit with your OpenAI API key (REQUIRED for AI image generation)
nano examples/.env

# Add your OpenAI API key:
OPENAI_KEY=your_actual_openai_api_key_here
```

### 5. Start the Server
```bash
# Make scripts executable
chmod +x start_server.sh

# Start the Flask application
./start_server.sh

# Or start the full-featured app manually (RECOMMENDED)
python app_1bit_working.py
```

### 6. Access Web Interface
Open your browser and navigate to:
```
http://your-pi-ip:5000
```

## 🎮 Usage

### 🎨 AI Image Generation
1. **Navigate to**: `http://your-pi-ip:5000`
2. **Enter a prompt**: *"A magical forest with glowing mushrooms"*
3. **Choose generation mode**:
   - **Generate & Display** - See your image immediately (~25 seconds)
   - **Generate Only** - Save to gallery for later (~15 seconds)

### 🖼️ Image Gallery Management  
1. **Browse Gallery** - View 185+ AI images with descriptions
2. **Display Images** - Click any image to show on e-Paper display
3. **Edit Descriptions** - Customize image descriptions for better organization
4. **Random Art** - Get instant inspiration with random image display

### 💻 Basic Display Controls
- **Clear Display** - Blank the screen
- **Test Pattern** - Show geometric shapes (1-bit B&W)
- **Hello World** - Display greeting message (1-bit B&W)  
- **Show Time** - Current date and time (1-bit B&W)
- **Custom Text** - Enter any message with word wrapping (1-bit B&W)

### 🔌 API Endpoints

#### 🎨 AI Image Generation
```http
POST /generate_image           # Generate and display image
POST /generate_image_only      # Generate and save to gallery

# Example:
{
  "prompt": "A serene mountain landscape with a lake"
}
```

#### 🖼️ Image Gallery Management
```http
GET  /images/list              # Browse all images with descriptions
GET  /images/random            # Display random image
POST /images/display           # Display specific image
POST /images/update_description # Update image description

# Example:
{
  "filename": "ai_custom_20250805_184711_resized.bmp"
}
```

#### 💻 Basic Display Controls
```http
GET  /                         # Main web interface
GET  /clear                    # Clear display
GET  /test                     # Show test pattern (1-bit B&W)
GET  /hello                    # Display "Hello World" (1-bit B&W)
GET  /time                     # Show current time (1-bit B&W)
POST /text                     # Display custom text (1-bit B&W)

# Example:
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
├── app_1bit_working.py            # 🌟 MAIN APPLICATION (Full-featured)
│                                  # ✨ AI image generation with DALL-E 3
│                                  # 🖼️ 185+ image gallery with descriptions
│                                  # 💻 Complete web interface
├── app_4bit.py                    # 4-bit grayscale app (display issues)
├── app_enhanced.py               # Enhanced version with web UI  
├── templates/                    # HTML templates
│   └── index.html               # Modern web interface with AI features
├── lib/                         # Waveshare EPD library
│   └── waveshare_epd/          # Display drivers
├── examples/                    # AI generation and quiz components
│   ├── harrypotter_quiz.py     # Interactive quiz with AI images
│   ├── helper_quiz.py          # Quiz helper functions
│   ├── image_generator.py      # AI image processing pipeline  
│   └── .env.example           # Environment template (OpenAI key)
├── pic/                        # Static image assets
└── CLAUDE.md                   # 📚 Comprehensive documentation
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