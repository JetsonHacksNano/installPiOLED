# installPiOLED
Install the Adafruit PiOLED 128x32 Monochrome OLED driver (3527)

Original article on JetsonHacks: https://wp.me/p7ZgI9-33H

The Adafruit PiOLED is a handy little display that connects to the Jetson Nano GPIO header. The display communicates with the Jetson over I2C, and is powered via the GPIO pins.

There are two scripts here, along with an file which displays information on the display. The file is pioled/stats.py. Gernerally you will modify the stats.py file to meet your needs. The default is to show the eth0 address, an updating GPU usage bar graph, memory usage and disk usage.

The first script, installPiOLED.sh will install the Adafruit-SSD1306 library. The SSD1306 is the driver chip for the PiOLED. Note that we use pip3 to install this library. Usage:

<blockquote>$ ./installPiOLED.sh</blockquote>

Once the library is installs, you can then run the example:

<blockquote>$ cd pioled<br>
$ python3 stats.py</blockquote>

If you would like to run the display stats app on system startup, the createService.sh script will install the stats app as a global library in /usr/local/lib/ as pioled, and create a startup service to launch. The startup service is in /etc/systemd/system/pioled_stats.service

To create the service:

<blockquote>$ ./createService.sh</blockquote>

You should consider filling out the setup.py file in the top directory more fully for your application. 
  
<h3>Notes</h3>

<h4>December, 2019</h4>
Initial Release

* Jetson Nano
* L4T 32.2.1/JetPack 4.2.2
