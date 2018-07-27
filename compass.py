import smbus
import time
import math
bus = smbus.SMBus(1)
address = 0x0d

for i in range(0,50):
	def read_byte(adr): #communicate with compass
	    return bus.read_byte_data(address, adr)

	def read_word(adr):
            high = bus.read_byte_data(address, adr)
            low = bus.read_byte_data(address, adr+1)
            print "high:",high
            print "low:",low
            val = ((high<<8)+low)
            print "value:",val
            return val

	def read_word_2c(adr):
            val = read_word(adr)
            if (val>= 0x8000):	
		return -((65535 - val)+1)
            else:
		return val

	def write_byte(adr,value):
		bus.write_byte_data(address, adr, value)
	
	write_byte(11, 0b01110000)
	write_byte(10, 0b00100000)
	write_byte(9, 0b00011101)
	scale = 0.92
	#x_offset = -10
	#y_offset = 10
	x_out = (read_word_2c(0)) * scale #calculating x,y,z coordinates
	y_out = (read_word_2c(2))* scale
	z_out = read_word_2c(4) * scale
	bearing = math.atan2(y_out, x_out) #0.48 is correction value
	if(bearing < 0):
            bearing += 2* math.pi
        print "Bearing:", math.degrees(bearing)
        print "x: ", x_out
        print "y: ", y_out
        print "z: ", z_out
	time.sleep(1)