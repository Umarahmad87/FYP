import smbus
import time
import math
import numpy as np
from scipy import stats
class Compass:
    def __init__(self):
        self.bus = smbus.SMBus(1)
        self.bus.write_byte_data(0x1E, 0x00, 0x60)
        self.bus.write_byte_data(0x1E, 0x02, 0x00)
        time.sleep(0.5)
    def getAngle(self):
        count = 0
        deg = []
        while True:
            data = self.bus.read_i2c_block_data(0x1E, 0x03, 6)
            xMag = data[0] * 256 + data[1]
            if xMag > 32767 :
                xMag -= 65536

            zMag = data[2] * 256 + data[3]
            if zMag > 32767 :
                zMag -= 65536

            yMag = data[4] * 256 + data[5]
            if yMag > 32767 :
                yMag -= 65536
            
            xMag = (xMag)
            yMag = (yMag)
            
            heading_rad = math.atan2(yMag, xMag)

 
            if(heading_rad < 0):
                heading_rad += 2 * math.pi
                
 
            if(heading_rad > 2 * math.pi):
                heading_rad -= 2 * math.pi
                
 
            heading_deg =int((heading_rad * 180 / math.pi)-2.40)
            deg.append(heading_deg)
            if count>=10:
                heading_deg = stats.mode(deg)[0][0]
                count = 0
                deg=[]
                return abs(360-heading_deg)
            time.sleep(0.01)
            count+=1
    def getReadings(self):
        data = self.bus.read_i2c_block_data(0x1E, 0x03, 6)
        xMag = data[0] * 256 + data[1]
        if xMag > 32767 :
            xMag -= 65536

        zMag = data[2] * 256 + data[3]
        if zMag > 32767 :
            zMag -= 65536

        yMag = data[4] * 256 + data[5]
        if yMag > 32767 :
            yMag -= 65536
        
        xMag = (xMag)
        yMag = (yMag)
        
        heading_rad = math.atan2(yMag, xMag)
    

        if(heading_rad < 0):
            heading_rad += 2 * math.pi

        if(heading_rad > 2 * math.pi):
            heading_rad -= 2 * math.pi

        heading_deg = (heading_rad * 180 / math.pi)-2.40
        
        return xMag,yMag,heading_deg
