
import serial, sys
from struct import pack
from time import sleep

s = serial.Serial('/dev/ttyACM0', 9600)
for i in range(255):
	s.write(pack('>2B', 1, i))
	sleep(.05)
