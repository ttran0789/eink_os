import subprocess
from PIL import Image, ImageDraw, ImageFont
from waveshare_epd import epd2in7_V2

def get_wifi_networks():
    try:
        output = subprocess.check_output(['nmcli', '-t', '-f', 'SSID', 'dev', 'wifi'])
        ssids = output.decode().splitlines()
        # Remove empty or duplicate SSIDs
        seen = set()
        cleaned = []
        for ssid in ssids:
            if ssid and ssid not in seen:
                cleaned.append(ssid)
                seen.add(ssid)
        return cleaned[:7]  # Limit to 7 to fit on screen
    except Exception as e:
        return [f"Error: {str(e)}"]

def display_networks(ssids):
    epd = epd2in7_V2.EPD()
    epd.init()
    epd.Clear()

    image = Image.new('1', (epd.width, epd.height), 255)
    draw = ImageDraw.Draw(image)

    font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf', 14)

    draw.text((10, 5), "Available Wi-Fi Networks:", font=font, fill=0)
    for i, ssid in enumerate(ssids):
        draw.text((10, 25 + i*20), ssid, font=font, fill=0)

    epd.display(epd.getbuffer(image))
    epd.sleep()

if __name__ == "__main__":
    networks = get_wifi_networks()
    display_networks(networks)
