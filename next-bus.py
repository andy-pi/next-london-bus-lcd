#!/usr/bin/python
#
# Name:         TfL Bus arrivals ticker for AndyPi LCD
# Developed by: AndyPi (http://andypi.co.uk/)
# Based on:     https://github.com/ismailuddin/raspberrypi/blob/master/tfl-bus-ticker/tfl-bus-ticker.py
# Date:         18/02/2016
# Version:      0.1

from TfLAPI import *
from AndyPi_LCD import AndyPi_LCD
import time, sys
from multiprocessing import Process

tfl = TfLBusArrivalsAPI()
lcd=AndyPi_LCD()
lcd.lcd_init()

def fetchBusArrivals(bSC):

	try:
		jsonObject = tfl.returnTfLJSON(bus_stop_code=bSC)
	except urllib2.URLError:
		print("Unable to connect to Internet...")

		
	busLineDestinationTime = []

	for entry in jsonObject:
		bLDT = []
		bLDT.append(entry['lineName'])
		bLDT.append(entry['destinationName'])
		bLDT.append(int(entry['timeToStation'])/60.0)
		busLineDestinationTime.append(bLDT)

	arrivalsList = sorted(busLineDestinationTime, key=lambda x:x[2])

	return arrivalsList


if __name__ == '__main__':
    
	#lcd.cls()
	location="LEWISHAM HOSPITAL"
	lcd.static_text(1,"l","From: ")
	lcd.static_text(2,"l",location)
	this_stop=tfl.searchBusStop(location) # returns a dictionary of stop codes for bus stop for those that fit the search criteria, could be more than one
	this_stop_code= this_stop[location] # get the code by lookup from the dictionary, if we know the name in advance
	#print "Bus Stop code for " + location + ": " + this_stop_code
	
	while True:
		arrivals = fetchBusArrivals(this_stop_code) # get JSON response for this bus stop code each time before we show the buses
		for bus in arrivals:
			bus_no=bus[0]
			bus_destination=bus[1]
			bus_mins_to_arrival= "in %.0f minutes" % (bus[2])
			line1=bus_no + " to " + bus_destination
		 	#tickerInfo = '%s to %s \nin %.0f minutes' % (bus[0], bus[1], bus[2])
			#print tickerInfo
			lcd.cls()
			lcd.static_text(2,"l",bus_mins_to_arrival)
			lcd.static_text(1,"l",line1)
			time.sleep(1)
			p = Process(target=lcd.scroll, args=(1,0.3, line1)) # start the process in a thread since scroll is blocking
			p.start()
			time.sleep(5)
			p.terminate()
