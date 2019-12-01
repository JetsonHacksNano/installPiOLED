#!/bin/bash
# Install the pioled_stats service for the Adafruit PiOLED (3527)
# The driver for the display is a SSD1306
# for NVIDIA Jetson Nano Developer Kit, L4T
# Copyright (c) 2019 Jetsonhacks 
# MIT License

python3 -m pip install --user --upgrade setuptools wheel
# Create a wheel installer for the stat program
sudo python3 setup.py sdist bdist_wheel
cd dist
sudo pip3 install pioled-1.0-py3-none-any.whl 
# Create the service, and start 'er up
cd ../utils
python3 create_stats_service.py
sudo mv pioled_stats.service /etc/systemd/system/pioled_stats.service
sudo systemctl daemon-reload
sudo systemctl enable pioled_stats
sudo systemctl start pioled_stats



