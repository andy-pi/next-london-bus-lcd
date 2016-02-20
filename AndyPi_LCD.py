#!/usr/bin/python
#
# HD44780 LCD Class for Raspberry Pi
#
# Developed by: AndyPi (http://andypi.co.uk/)
# Based on work by Raspi Forum Members: Matt Hawkins + Texy
#
# Date : 27/03/2013
# Version 1.1 (changed wiringpi setup to Sys not Gpio


import time
from datetime import datetime

class AndyPi_LCD:

  # Define GPIO to LCD mapping
  LCD_RS = 7
  LCD_E  = 8
  LCD_D4 = 25
  LCD_D5 = 24
  LCD_D6 = 23
  LCD_D7 = 14
  LCD_LED = 18

  # Define constants
  LCD_WIDTH = 16    # Maximum characters per line
  LCD_CHR = True
  LCD_CMD = False
  LCD_LINE_1 = 0x80 # LCD memory address for the 1st line
  LCD_LINE_2 = 0xC0 # LCD memory address for the 2nd line 

  # Timing constants
  E_PULSE = 0.00005
  E_DELAY = 0.00005
  
  # import wiringpi class
  import wiringpi
  #  import GPIO class
  import RPi.GPIO as GPIO

  # Setup GPIO 
  GPIO.setmode(GPIO.BCM)       # Use BCM GPIO numbers
  GPIO.setwarnings(False)
  GPIO.setup(LCD_E, GPIO.OUT)  # E
  GPIO.setup(LCD_RS, GPIO.OUT) # RS
  GPIO.setup(LCD_D4, GPIO.OUT) # DB4
  GPIO.setup(LCD_D5, GPIO.OUT) # DB5
  GPIO.setup(LCD_D6, GPIO.OUT) # DB6
  GPIO.setup(LCD_D7, GPIO.OUT) # DB7
  wiringpi.wiringPiSetupSys() # was .wiringPiSetupGpio()

  	
  def main(self):
    # Send a test text
    self.lcd_init()
    self.led(512)
    self.scroll_clock(1,"c",0.5,"AndyPi LCD Test Message")

  def lcd_init(self):
    # Initialise display
    self.lcd_byte(0x33,self.LCD_CMD)  # init
    self.lcd_byte(0x32,self.LCD_CMD)  # init
    self.lcd_byte(0x28,self.LCD_CMD)  # 2 line 5x7 matrix
    self.lcd_byte(0x0C,self.LCD_CMD)  # turn cursor off (0x0E to enable)
    self.lcd_byte(0x06,self.LCD_CMD)  # move cursor right
    self.lcd_byte(0x01,self.LCD_CMD)  # clear display

  def cls(self):
    self.lcd_byte(0x01,self.LCD_CMD)  # clear display
    self.led(0) # turn off backlight

  def static_text(self,line,just,message):
    # set justification
    if just=="l":
      message = message.ljust(self.LCD_WIDTH," ")

    elif just=="r":
      message = message.rjust(self.LCD_WIDTH," ")

    elif just=="c":
      message = message.center(self.LCD_WIDTH," ")
    
    time.sleep(0.01)
    # set which line to print to
    if line==1:line=self.LCD_LINE_1
    elif line==2:line=self.LCD_LINE_2
    self.lcd_byte(line,self.LCD_CMD)
    # send string to display
    for i in range(self.LCD_WIDTH):
      self.lcd_byte(ord(message[i]),self.LCD_CHR)
    
  def scroll(self,line,s, scrollmsg):
    # scroll display
    scrollmsg = (scrollmsg+"   |   ") * 200
    z=0
    try:
      while z < len(scrollmsg):
        self.static_text(line,"l", scrollmsg[z:(z+16)])
        time.sleep(s)
        z=z+1
        if z==len(scrollmsg):
          z=0
    except KeyboardInterrupt:
      self.cls()

  def clock(self,line,just):
    if line==1:line=self.LCD_LINE_1
    elif line==2:line=self.LCD_LINE_2
    try:
      while True:
        self.static_text(line,just,(datetime.now().strftime('%H:%M:%S')))
        #(datetime.now().strftime('%a %d %b %y'))
        time.sleep(1)
    except KeyboardInterrupt:
        self.cls()


  def scroll_clock(self,line,just,s, scrollmsg1):
    # scroll display
    scrollmsg1 = (scrollmsg1+"   |   ") * 200
    z=0
    if line==1:line_2=2
    elif line==2:line_2=1
    try:
      while z < len(scrollmsg1):
        self.static_text(line_2,"l", scrollmsg1[z:(z+16)])
        x=datetime.now().strftime('%H:%M')
        self.static_text(line,just,x)
        time.sleep(s)
        z=z+1
        if z==len(scrollmsg1):
          z=0
    except KeyboardInterrupt:
      self.cls()

  def led(self,led_value):
    if led_value==0:
      self.wiringpi.pinMode(self.LCD_LED, 1) # turn off LED
    else:   
      self.wiringpi.pinMode(self.LCD_LED, 2) # LED set up as PWM
      self.wiringpi.pwmWrite(self.LCD_LED, led_value)

  def lcd_byte(self,bits, mode):
    # Send byte to data pins
    # bits = data
    # mode = True  for character
    #        False for command

    self.GPIO.output(self.LCD_RS, mode) # RS

    # High bits
    self.GPIO.output(self.LCD_D4, False)
    self.GPIO.output(self.LCD_D5, False)
    self.GPIO.output(self.LCD_D6, False)
    self.GPIO.output(self.LCD_D7, False)
    if bits&0x10==0x10:
      self.GPIO.output(self.LCD_D4, True)
    if bits&0x20==0x20:
      self.GPIO.output(self.LCD_D5, True)
    if bits&0x40==0x40:
      self.GPIO.output(self.LCD_D6, True)
    if bits&0x80==0x80:
      self.GPIO.output(self.LCD_D7, True)

    # Toggle 'Enable' pin
    time.sleep(self.E_DELAY)    
    self.GPIO.output(self.LCD_E, True)  
    time.sleep(self.E_PULSE)
    self.GPIO.output(self.LCD_E, False)  
    time.sleep(self.E_DELAY)      

    # Low bits
    self.GPIO.output(self.LCD_D4, False)
    self.GPIO.output(self.LCD_D5, False)
    self.GPIO.output(self.LCD_D6, False)
    self.GPIO.output(self.LCD_D7, False)
    if bits&0x01==0x01:
      self.GPIO.output(self.LCD_D4, True)
    if bits&0x02==0x02:
      self.GPIO.output(self.LCD_D5, True)
    if bits&0x04==0x04:
      self.GPIO.output(self.LCD_D6, True)
    if bits&0x08==0x08:
      self.GPIO.output(self.LCD_D7, True)

    # Toggle 'Enable' pin
    time.sleep(self.E_DELAY)    
    self.GPIO.output(self.LCD_E, True)  
    time.sleep(self.E_PULSE)
    self.GPIO.output(self.LCD_E, False)  
    time.sleep(self.E_DELAY)   

if __name__ == '__main__':
  lcd=AndyPi_LCD()
  lcd.main()
