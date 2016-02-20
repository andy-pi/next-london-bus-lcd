# Next London Bus LCD
Use the TfL API to get details of the next buses arriving at your London location, and display it on your AndyPi HD44780 LCD. Based on work here: https://github.com/ismailuddin/raspberrypi/blob/master/tfl-bus-ticker/TfLAPI.py

## Hardware
Raspberry Pi (tested on v1 B+)
AndyPi LCD (connection as per: http://andypi.co.uk/?p=300) or compatible HD44780 LCD

## Installation (test on Raspberry Pi 1 B+)
Grab the repo and install
```
git clone https://github.com/andy-pi/next-london-bus-lcd.git
cd next-london-bus-lcd
sudo pip install virtualenv
virtualenv env
source env/bin/activate
pip install RPi.GPIO
```
Test the LCD module works:
```
source env/bin/activate
python AndyPiLCD.py
```
Run the program
```
python next-bus.py
```