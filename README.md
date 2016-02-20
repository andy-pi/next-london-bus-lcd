# Next London Bus LCD
Use the TfL API to get details of the next buses arriving at your London location, and display it on your AndyPi HD44780 LCD

## Todo
Since it was a few years ago I wrote the AndyPi_LCD class, and the GPIO functions have been update
the wiringpi PWM implementation seems to have broken the led function, so need to look into this.

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
pip install wiringpi
pip install RPi.GPIO
```
Test the LCD module works:
```
source env/bin/activate
python AndyPiLCD.python
```
Run the program
```
python next-bus.py
```