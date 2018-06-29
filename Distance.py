import math
from numpy import *
import cv2
class CDistance:
    def __init__(self):
        self.obj_dist = -1
    def calculate_distance(self,frame):
        print 'frame.type=',type(frame)
        if frame==None:
            print 'Frame is empty'
            return frame,0,0
        #frame = cv2.circle(frame, (320, 240), 1, (255,0,0), 3)
        print 'frame.shape=',frame.shape
        num = (frame[:,:,2] <= 255) & (frame[:,:,2] >= 230) & (frame[:,:,0] <= 150) & (frame[:,:,0] >= 0) & (frame[:,:,1] <= 160) & (frame[:,:,1] >= 0)
        print 'num:',num
        print 'num.shape:',num.shape
        xy_val =  num.nonzero()
        print "xyLen=",len(xy_val)
        x_val = median(xy_val[0])
        y_val = median(xy_val[1])
        print 'x:',x_val
        print 'y:',y_val
        if not(math.isnan(x_val) or math.isnan(y_val)): 
                print 'RGB:',frame[int(x_val),int(y_val)]
                #frame = cv2.circle(frame, (int(y_val), int(x_val)), 5, (0,0,255), 3)
                
                dist = ((x_val - 320)**2 + (y_val - 240)**2 )**0.5 # distance of dot from center pixel
                #dist = abs(x_val - 320) # distance of dot from center x_axis only

                print " dist from center pixel is " + str(dist)

                # work out distance using D = h/tan(theta)

                theta =0.00148933*dist + 0.11908426
                tan_theta = math.tan(theta)

                if tan_theta > 0: # bit of error checking
                        self.obj_dist =  int(21.0 / tan_theta)

                        print "\033[12;0H" + "the dot is " + str(self.obj_dist) + "cm  away"
                        return frame,x_val,y_val
        return frame,0,0
