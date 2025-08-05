#!/usr/bin/python
# -*- coding:utf-8 -*-
import sys
import os
picdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'pic')
libdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'lib')
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
    
    '''2Gray(Black and white) display'''
    logging.info("init and Clear")
    epd.init()
    epd.Clear()
    font24 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 24)
    font18 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 18)
    font35 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 35)
    
    # Drawing on the Horizontal image
    logging.info("4.Drawing on the Horizontal image...")
    Himage = Image.new('1', (epd.height, epd.width), 255)  # 255: clear the frame
    draw = ImageDraw.Draw(Himage)

    # Draw hello world
    draw.text((10, 0), 'hello world', font = font24, fill = 0)
    epd.display_Base(epd.getbuffer(Himage))
    time.sleep(2)

    #### Initialize the font and image for partial update
    epd.init()   

    # blah
    draw.rectangle((10, 50, 120, 90), fill = 255)
    draw.text((10, 50), 'Line 2', font = font18, fill = 0)
    epd.display_Partial(epd.getbuffer(Himage),50, epd.height - 90, 90, epd.height - 10)
    time.sleep(2)   


    # partial update (WORKING)
    num = 0
    while (True):
        draw.rectangle((10, 110, 120, 150), fill = 255)
        draw.text((10, 110), time.strftime('%H:%M:%S'), font = font24, fill = 0)
        # newimage = Himage.crop([10, 110, 120, 150])
        # Himage.paste(newimage, (10,110)) 
        epd.display_Partial(epd.getbuffer(Himage),110, epd.height - 120, 150, epd.height - 10)
        num = num + 1
        if(num == 10):
            break
   
    logging.info("Goto Sleep...")
    epd.sleep()
        
except IOError as e:
    logging.info(e)
    
except KeyboardInterrupt:    
    logging.info("ctrl + c:")
    epd2in7_V2.epdconfig.module_exit(cleanup=True)
    exit()
