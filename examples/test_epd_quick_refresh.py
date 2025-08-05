#!/usr/bin/python
# -*- coding:utf-8 -*-
import sys
import os
if '__file__' in globals():
    base_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
else:
    # Fallback for environments like VSCode interactive or notebooks
    base_dir = os.path.dirname(os.path.dirname(os.path.realpath(os.getcwd())))
picdir = os.path.join(base_dir, 'pic')
libdir = os.path.join(base_dir, 'lib')
if os.path.exists(libdir):
    sys.path.append(libdir)

import logging
from waveshare_epd import epd2in7_V2
import time
from PIL import Image,ImageDraw,ImageFont
import traceback

logging.basicConfig(level=logging.DEBUG)

try:

    logging.info("epd2in7 Demo")   
    epd = epd2in7_V2.EPD()
    epd.init()
    
    font24 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 24)
    font18 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 18)
    font35 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 35)
    

    # Quick refresh
    logging.info("Quick refresh demo")
    epd.init_Fast()
    # epd.Clear()

    # Drawing on the Horizontal image
    logging.info("4.Drawing on the Horizontal image...")
    Himage = Image.new('1', (epd.height, epd.width), 255)  # 255: clear the frame
    draw = ImageDraw.Draw(Himage)
    # draw.text((10, 0), 'hello world', font = font24, fill = 0)
    epd.display_Base(epd.getbuffer(Himage))
    # time.sleep(2)
    






    logging.info("5.show time")
    epd.init()   
    '''
    # If you didn't use the EPD_2IN7_V2_Display_Base() function to refresh the image before,
    # use the EPD_2IN7_V2_Display_Base_color() function to refresh the background color, 
    # otherwise the background color will be garbled 
    '''
    # epd.display_Base_color(0xff)
    Himage = Image.new('1', (epd.height ,epd.width), 0xff)
    draw = ImageDraw.Draw(Himage)
    # num = 0
    # while (True):
    #     draw.rectangle((10, 110, 120, 150), fill = 255)
    #     draw.text((10, 110), time.strftime('%H:%M:%S'), font = font24, fill = 0)
    #     text_width, text_height = draw.textsize(time.strftime('%H:%M:%S'), font=font24)
    #     epd.display_Partial(epd.getbuffer(Himage),110, epd.height - 120, 150, epd.height - 10)
    #     print(f'Displaying partial from 10, {epd.height - 120} to 110, {epd.height - 10}')
    #     print(f'Text size for time: {text_width}x{text_height}')
    #     num = num + 1
    #     if(num == 3):
    #         break

    

    # draw.text((10, 10), "Hello World", font = font18, fill = 0)
    # epd.display_Partial(epd.getbuffer(Himage), 10, epd.height - 120, 250, epd.height - 10)
    

    # Text content and position
    text = "Hello World"
    x, y = 10, 10  # top-left position for the text

    # Draw rectangle
    draw.rectangle((x, y, x + 200, y + 30), fill=255)

    # Draw the text
    draw.text((x, y), text, font=font18, fill=0)

    # Perform a partial refresh for just the bounding box
    epd.display_Partial(epd.getbuffer(Himage), x, y, x + 200, y + 30)  # Adjust the bounding box as needed


    # # partial update

    # # Test Write Multiple Lines with 3 seconds interval
    # test_lines = ["Test line 1", "Test line 2", "Test line 3"]


    # # 4. Draw the first line at (10, 10)
    # draw.rectangle((10, 10, 200, 30), fill=255)  # Clear the area first
    # draw.text((10, 10), test_lines[0], font=font18, fill=0)

    # # 5. Display just that area
    # epd.display_Partial(epd.getbuffer(Himage), 10, 10, 50, 100)  # adjust 200x30 if needed

    # # Wait 1 second
    # time.sleep(1)



    logging.info("Goto Sleep...")
    epd.sleep()
        
except IOError as e:
    logging.info(e)
    
except KeyboardInterrupt:    
    logging.info("ctrl + c:")
    epd2in7_V2.epdconfig.module_exit(cleanup=True)
    exit()
