import math
from numpy import *
import cv2
class CDistance:
    def __init__(self):
        self.obj_dist = -1
    def calculate_distance(self,frame):
        try:
            num = (frame[:,:,2] <= 255) & (frame[:,:,2] >= 200) & (frame[:,:,0] <= 180) & (frame[:,:,0] >= 0) & (frame[:,:,1] <= 180) & (frame[:,:,1] >= 0)
            xy_val =  num.nonzero()
            x_val = median(xy_val[1])
            y_val = median(xy_val[0])
            if not(math.isnan(x_val) or math.isnan(y_val)): 
                    
                    dist = ((x_val - 160)**2 + (y_val - 120)**2 )**0.5
                    #print " dist from center pixel is " + str(dist)
                    theta =0.0029371160484085597*dist + 0.07962586307503382
                    tan_theta = math.tan(theta)
                    if tan_theta > 0:
                            self.obj_dist =  int(3.50 / tan_theta)
                            #print "the dot is " + str(self.obj_dist) + "cm  away"
                            return frame,x_val,y_val,self.obj_dist
            print "not detected"
            return frame,0,0,100
        except:
            print "exception frame empty"
            return frame,0,0,100
