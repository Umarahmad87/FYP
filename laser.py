import cv2
from numpy import *
import math
 
#variables
loop = 1
dot_dist = 0
 
cv2.namedWindow("preview")
vc = cv2.VideoCapture(0)
 
if vc.isOpened(): # try to get the first frame
    rval, frame = vc.read() 
else:
    rval = False
    #print "failed to open webcam"
if rval == 1 :
 
    while loop == 1:
		cv2.imshow("preview", frame)
		rval, frame = vc.read()
		print 'fr.shape:',frame.shape
		frame = cv2.circle(frame, (320, 240), 1, (255,0,0), 3)
		key = cv2.waitKey(20)
		if key == 27: # exit on ESC
			loop = 0
		#frame[where((frame>=[0,0,254]).all(axis=2))] = [10,10,10]
		#num = (frame[:,:,2] >= 253)
		#num = (frame[:,:,[0,1,2]] >= (0,0,253)) & (frame[:,:,[0,1,2]] <= (50,50,255)) #[:,[0,1]]<(250,250)
		#num = (frame >= (0,0,230)) & (frame <= (50,50,255))
		num = (frame[:,:,2] <= 255) & (frame[:,:,2] >= 210) & (frame[:,:,0] <= 180) & (frame[:,:,0] >= 0) & (frame[:,:,1] <= 180) & (frame[:,:,1] >= 0)
		print 'shape:',num.shape
		#num2 = (frame[:,:,[0,1,2]] >= (250,250,253))
		
		#num=logical_and(logical_and(num[:,0],num[:,1]),num[:,2])
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
			frame = cv2.circle(frame, (int(y_val), int(x_val)), 5, (0,0,255), 3)
			
			dist = ((x_val - 320)**2 + (y_val - 240)**2 )**0.5 # distance of dot from center pixel
			#dist = abs(x_val - 320) # distance of dot from center x_axis only

			print " dist from center pixel is " + str(dist)

			# work out distance using D = h/tan(theta)

			theta =0.00148933*dist + 0.11908426
			tan_theta = math.tan(theta)

			if tan_theta > 0: # bit of error checking
				obj_dist =  int(21.0 / tan_theta)

				print "\033[12;0H" + "the dot is " + str(obj_dist) + "cm  away"
elif rval == 0:
        print " webcam error "
