import smbus
import time
import math
import numpy as np

class Compass:
    
    def __init__(self):
        self.bus = smbus.SMBus(1)
        self.address = 0x0d

    def read_byte(self,adr): #communicate with compass
            return self.bus.read_byte_data(self.address, adr)

    def read_word(self,adr):
            high = self.bus.read_byte_data(self.address, adr)
            low = self.bus.read_byte_data(self.address, adr+1)
            val = ((high<<8)+low)
            return val

    def read_word_2c(self,adr):
        val = self.read_word(adr)
        if (val>= 0x8000):	
            return -((65535 - val)+1)
        else:
            return val

    def write_byte(self,adr,value):
            self.bus.write_byte_data(self.address, adr, value)

    def get_BXYZ(self):
        
        self.write_byte(11, 0b01110000)
	self.write_byte(10, 0b00100000)
	self.write_byte(9, 0b00011101)
	scale = 0.92
	x_offset = 114
	y_offset = -122
	x_out = (self.read_word_2c(0)- x_offset) * scale #calculating x,y,z coordinates
	y_out = (self.read_word_2c(2)- y_offset)* scale
	z_out = self.read_word_2c(4) * scale
	bearing = math.atan2(y_out, x_out)+0.5 #0.48 is correction value
	#print "lllb:",bearing
	if(bearing < 0):
            bearing += 2* math.pi
        return math.degrees(bearing)-2, x_out, y_out, z_out
    
c = Compass()
count = 0
val = []
while True:
    b,x,y,z = c.get_BXYZ()
    val.append(b)
    if count==10:
        count=0
        g = np.mean(val)
        print "Bearing:",g
        print "X:",x
        print "Y:",y
        print "z:",z
    count+=1
    time.sleep(0.1)
    