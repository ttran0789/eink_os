from PIL import Image
import time
import sys
import os
from dotenv import load_dotenv
from openai import OpenAI
import requests

# Load environment variables from .env file
load_dotenv()

# Set OpenAI API key
client = OpenAI(api_key=os.getenv("OPENAI_KEY"))

# Path to the Waveshare library
sys.path.append('/home/pi/e-Paper/RaspberryPi_JetsonNano/python/lib')
from waveshare_epd import epd2in7_V2  # Use the correct driver





# Generate an image based on a topic using OpenAI's DALL·E API
def generate_image(topic, filepath):
    print("Generating image...")
    # Request a 3:2 aspect ratio, minimal size, black and white image
    response = client.images.generate(
        model="dall-e-3",
        prompt=f"Illustration about '{topic}', minimal colors, minimalistic, reduce small details.",
        n=1,
        size="1024x1024",  # Larger 3:2 aspect ratio (width:height)
        response_format="url"
    )

    # Download the image
    image_url = response.data[0].url
    img_data = requests.get(image_url).content

    # Save the image
    with open(filepath, 'wb') as handler:
        handler.write(img_data)

    # # Convert to black and white using PIL
    # img = Image.open(filepath).convert('1')
    # img.save(filepath)

    print(f"Image saved to {filepath}")


# Crop the image to a 3:2 aspect ratio
def crop_image_3_2(filepath, filepath_new):
    img = Image.open(filepath)
    width, height = img.size
    target_ratio = 3 / 2  # width / height
    current_ratio = width / height

    if current_ratio > target_ratio:
        # Image is too wide → crop width
        new_width = int(height * target_ratio)
        left = (width - new_width) / 2
        top = 0
        right = left + new_width
        bottom = height
    else:
        # Image is too tall or square → crop height
        new_height = int(width / target_ratio)
        top = (height - new_height) / 2
        left = 0
        right = width
        bottom = top + new_height

    img_cropped = img.crop((left, top, right, bottom))
    img_cropped.save(filepath_new)
    print(f"Image cropped to 3:2 aspect ratio and saved to {filepath_new}")

# Resize image down to fit the e-Paper display: 264x176 pixels
def resize_image(filepath, filepath_new):
    img = Image.open(filepath)
    img_resized = img.resize((264, 176), Image.ANTIALIAS)
    img_resized.save(filepath_new)
    print(f"Image resized to fit e-Paper display and saved to {filepath_new}")

# Function to convert image to 4-bit bitmap format
def convert_to_4bit(filepath,filepath_new):
    img = Image.open(filepath)
    img = img.convert('L')  # Convert to grayscale

    # Quantize to 4 grayscale levels (0, 85, 170, 255)
    def quantize_4gray(x):
        if x < 64:
            return 0
        elif x < 128:
            return 85
        elif x < 192:
            return 170
        else:
            return 255

    img = img.point(quantize_4gray, 'L')
    img.save(filepath_new, format='BMP')
    print(f"Image converted to 4-color grayscale and saved to {filepath_new}")

# Display the image on the e-Paper display
def display_image(filepath):
    epd = epd2in7_V2.EPD()
    epd.init()
    epd.Clear()

    # Load image
    img = Image.open(filepath)

    # Crop to 3:2 aspect ratio
    width, height = img.size
    target_ratio = 3 / 2
    current_ratio = width / height

    if current_ratio > target_ratio:
        # Crop width
        new_width = int(height * target_ratio)
        left = (width - new_width) // 2
        top = 0
        img = img.crop((left, top, left + new_width, height))
    else:
        # Crop height
        new_height = int(width / target_ratio)
        top = (height - new_height) // 2
        left = 0
        img = img.crop((left, top, width, top + new_height))

    # Rotate for landscape and resize to display size
    img = img.rotate(90, expand=True).resize((epd.width, epd.height)).convert('1')

    # Display
    epd.display(epd.getbuffer(img))
    time.sleep(2)
    epd.sleep()
    print(f"Image displayed on e-Paper display from {filepath}")

# def display_image_4bit(filepath):
#     epd = epd2in7_V2.EPD()
#     epd.Init_4Gray()
#     epd.Clear()

#     # Load Image
#     HImage = Image.open(filepath)

#     # Display the image
#     epd.display_4Gray(epd.getbuffer_4Gray(HImage))


if __name__ == "__main__":
    
    # Example usage
    topic = r"man working on a shuttle bus with his buttcrack showing"

    filepath = "/home/pi/rpi-screen/ai_gen_image.bmp"
    filepath_new = "/home/pi/rpi-screen/ai_gen_image_crop.bmp"
    filepath_resized = "/home/pi/rpi-screen/ai_gen_image_resized.bmp"
    filepath_4bit = "/home/pi/rpi-screen/ai_gen_image_4bit.bmp"

    # Generate the image
    generate_image(topic, filepath)
    # filepath = "/home/pi/rpi-screen/shahtzee.PNG"

    # Crop the image to 3:2 aspect ratio
    crop_image_3_2(filepath, filepath_new)

    # Resize image down to fit the e-Paper display: 264x176 pixels
    resize_image(filepath_new, filepath_resized)

    # Convert to 4-bit bitmap format
    convert_to_4bit(filepath_resized, filepath_4bit)

    # Function to display the image on the e-Paper display
    display_image(filepath_4bit)
    


# # Init
# epd = epd2in7_V2.EPD()
# epd.init()
# epd.Clear()

# # Load and prepare image
# fp_lola_img = '/home/pi/rpi-screen/lola2.bmp'
# image = Image.open(fp_lola_img).resize((epd.height, epd.width)).convert('1')

# # Show the image
# epd.display(epd.getbuffer(image))

# # Sleep
# time.sleep(2)
# epd.sleep()
