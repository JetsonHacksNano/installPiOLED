#!/bin/bash
# Install the driver for the Adafruit PiOLED (3527)
# The driver for the display is a SSD1306
# for NVIDIA Jetson Nano Developer Kit, L4T
# Copyright (c) 2019 Jetsonhacks 
# MIT License

# Set our access to I2C permissions
sudo usermod -aG i2c $USER
sudo udevadm control --reload-rules && sudo udevadm trigger
sudo apt-get update
sudo apt install python3-pip python3-pil -y
# Install the Adafruit library for the SSD1306 OLED driver
# Note that Adafruit-SSD1306 library is deprecated; newer versions of
# the library use CircuitPython
pip3 install Adafruit-SSD1306
# We should be able to access the PiOLED now
# Note that we may have to reboot for the i2c change to take effect




