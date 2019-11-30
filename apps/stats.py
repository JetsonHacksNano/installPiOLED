#! /usr/bin/python3
# Copyright (c) 2017 Adafruit Industries
# Author: Tony DiCola & James DeVito
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
# Portions copyright (c) NVIDIA 2019
# Portions copyright (c) JetsonHacks 2019

import time

import Adafruit_SSD1306

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
# from jetbot.utils.utils import get_ip_address

import subprocess

def get_ip_address(interface):
    if get_network_interface_state(interface) == 'down':
        return None
    cmd = "ifconfig %s | grep -Eo 'inet (addr:)?([0-9]*\.){3}[0-9]*' | grep -Eo '([0-9]*\.){3}[0-9]*' | grep -v '127.0.0.1'" % interface
    return subprocess.check_output(cmd, shell=True).decode('ascii')[:-1]

# Return a float representing the percentage of GPU being used.
# On the Jetson Nano, the GPU is GPU0
def get_gpu_usage():
    GPU = 0.0
    with open ("/sys/devices/gpu.0/load", encoding="utf-8") as gpu_file:
      GPU=gpu_file.readline()
      GPU=int(GPU)/10
    return GPU


def get_network_interface_state(interface):
    return subprocess.check_output('cat /sys/class/net/%s/operstate' % interface, shell=True).decode('ascii')[:-1]


# 128x32 display with hardware I2C:
disp = Adafruit_SSD1306.SSD1306_128_32(rst=None, i2c_bus=1, gpio=1) # setting gpio to 1 is hack to avoid platform detection

# Initialize library.
disp.begin()

# Clear display.
disp.clear()
disp.display()

# Create blank image for drawing.
# Make sure to create image with mode '1' for 1-bit color.
width = disp.width
height = disp.height
image = Image.new('1', (width, height))

# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)

# Draw a black filled box to clear the image.
draw.rectangle((0,0,width,height), outline=0, fill=0)

# Draw some shapes.
# First define some constants to allow easy resizing of shapes.
padding = -2
top = padding
bottom = height-padding
# Move left to right keeping track of the current x position for drawing shapes.
x = 0

# Load default font.
font = ImageFont.load_default()


while True:

    # Draw a black filled box to clear the image.
    draw.rectangle((0,0,width,height), outline=0, fill=0)

    # Shell scripts for system monitoring from here : https://unix.stackexchange.com/questions/119126/command-to-display-memory-usage-disk-usage-and-cpu-load
    cmd = "top -bn1 | grep load | awk '{printf \"CPU Load: %.2f\", $(NF-2)}'"
    CPU = subprocess.check_output(cmd, shell = True )
    cmd = "free -m | awk 'NR==2{printf \"Mem: %s/%sMB %.2f%%\", $3,$2,$3*100/$2 }'"
    MemUsage = subprocess.check_output(cmd, shell = True )
    cmd = "df -h | awk '$NF==\"/\"{printf \"Disk: %d/%dGB %s\", $3,$2,$5}'"
    Disk = subprocess.check_output(cmd, shell = True )

    # Print the IP address 
    # Two examples here, wired and wireless 
    draw.text((x, top),       "eth0: " + str(get_ip_address('eth0')),  font=font, fill=255)
    # draw.text((x, top+8),     "wlan0: " + str(get_ip_address('wlan0')), font=font, fill=255)

    # Draw the GPU usage as a bar graph
    # draw.text((x, top+8),     "GPU:  " +"{:3.1f}".format(GPU)+" %", font=font, fill=255)
    string_width, string_height=font.getsize("GPU:  ")
    # Figure out the width of the bar
    full_bar_width=width-(x+string_width)-1
    gpu_usage=get_gpu_usage()
    # Avoid divide by zero ...
    if gpu_usage == 0.0 :
       gpu_usage=0.001
    draw_bar_width=int(full_bar_width*(gpu_usage/100))
    draw.text((x, top+8),     "GPU:  ", font=font, fill=255)
    draw.rectangle((x+string_width,top+12,x+string_width+draw_bar_width,top+14), outline=1, fill=1)

    # Show the memory Usage
    # The MemUsage string is too long to display, we cut it down some here
    mem_usage=MemUsage.decode('utf-8').split()
    # slice off the last character (which is a % character)
    mem_percent_use=float(mem_usage[2][:-1])
    draw.text((x, top+16),mem_usage[0]+" "+"{:3.0f}".format(mem_percent_use)+"%"+" "+mem_usage[1], font=font, fill=255)
    # draw.text((x, top+16),    str(MemUsage.decode('utf-8')),  font=font, fill=255)
    # Show the amount of disk being used
    draw.text((x, top+25),    str(Disk.decode('utf-8')),  font=font, fill=255)

    # Display image.
    disp.image(image)
    disp.display()
    # Update 4x a second; 1 = 1 second
    time.sleep(0.25)
