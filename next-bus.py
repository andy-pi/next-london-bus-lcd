# Title:         TfL Bus arrivals ticker for AndyPi LCD
# Developed by: AndyPi (http://andypi.co.uk/)
# Based on:     https://github.com/ismailuddin/raspberrypi/blob/master/tfl-bus-ticker/tfl-bus-ticker.py
# Date:         18/02/2016
# Version:      1.0

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
    
	lcd.cls()
	lcd.led(1)
	location="LEWISHAM HOSPITAL"
	lcd.static_text(1,"l","From: ")
	lcd.static_text(2,"l",location)
	# returns a dictionary of stop codes for stops that fit the search criteria, could > 1
	this_stop=tfl.searchBusStop(location)
	# get the code by lookup from the dictionary, if we know the name in advance
	this_stop_code= this_stop[location] 
	# we can print this here if we're just searching
	# print "Bus Stop code for " + location + ": " + this_stop_code
	
	while True:
		# we'll use out this_stop_code which we looked up as an input
		# it will fail if there is more than one stop returned !
		# get JSON response for this bus stop code each time before we show the buses
		arrivals = fetchBusArrivals(this_stop_code) 
		for bus in arrivals:
			bus_no = bus[0]
			bus_destination = bus[1]
			bus_mins_to_arrival = "in %.0f minutes" % (bus[2])
			line1 = bus_no + " to " + bus_destination

			lcd.static_text(2,"l",bus_mins_to_arrival)
			lcd.static_text(1,"l",line1)
			time.sleep(1)
			# start the process in a thread since scroll is a blocking function
			p = Process(target=lcd.scroll, args=(1,0.3, line1)) 
			p.start()
			time.sleep(5)
			p.terminate()
