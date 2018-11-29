from robot import *
import threading
from Queue import Queue
import os
import random
from Robot_Canvas import *
from imu import *


R = 0
DL = 0
DR = 0
D = 0
canvas = 0
tstop = Queue(maxsize=1)
port1 = 1215
class obstacleAvoidence:

    def rotate(self,deg,direction='right'):
    #print 'deg:',
        global R
        global DL
        global DR
        global D
        global canvas
        print 'In rotate'
        angle,poll_interval= getAngle()
        print 'angle:',angle
        angle = int(angle)
        if direction=='right':
            target_angle = angle + deg
            target_angle = target_angle%360
        else:
            target_angle = angle - deg
            if target_angle<0:
                target_angle=360-abs(target_angle)
            else:
                target_angle%=360

        print 'target_angle:',target_angle,' current_angle:',angle   

        
        if target_angle>360:
            target_angle -= 360 
        if target_angle<0:
            target_angle += 360
        medAngle = []
        while True:
            R.right(0.16,speed=60)
            #time.sleep(10)
            time.sleep(poll_interval*1.0/1000.0)
            current_angle,_ = getAngle()
            print 'target_angle:',target_angle,' current_angle:',current_angle
            try:
                distance = [int(DL.sonic_distance()),int(D.sonic_distance()),
                            int(DR.sonic_distance())]
            except:
                print 'Except in sonic'
            print 'distance:',distance
            r_angle = current_angle+22
            l_angle = current_angle-22
            if r_angle>360:
                r_angle -= 360 
            if r_angle<0:
                r_angle += 360
        
            if l_angle>360:
                l_angle -= 360 
            if l_angle<0:
                l_angle += 360    
            
            canvas.update_position([l_angle,
                                    current_angle,r_angle],distance,rot_bool=True)
            if( abs(current_angle-target_angle)<15):
                canvas.close_connection()
                break
            
    def make_move(self):
                
        try:
            global R
            global DL
            global DR
            global D
            global canvas
            
            R = RoboMovement()
            DL = DistanceCalculation(pin=[40,38])
            DR = DistanceCalculation(pin=[36,32])
            D = DistanceCalculation(pin=[18,16])
            print 'Canvas Ini'
            
            R.setup()
            canvas = Canvas('192.168.0.193 ',port1)
            print 'Canvas created'
            count = 5
            dist = 0
            global tstop
            choice = [R.left,R.right,R.left,R.right,R.left,R.right,R.left,R.right]
            
            while True:
                try:
                    dist = DL.sonic_distance()
                    #print "Distance Left= ",dist
                    dist2 = DR.sonic_distance()
                    #print "Distance Right= ",dist2
                    dist3 = D.sonic_distance()
                    #print "Distance forward= ",dist3
                    angle,poll_interval = getAngle()
                    #print("Heading",angle)
                    #print "poll",poll_interval
                    self.rotate(350,'right')
                    #self.checkObstacle(dist,dist3,dist2)
                    
                    break
                    time.sleep(poll_interval*1.0/1000.0)
                                    
                    stop = tstop.get(False)
                    if(stop==False):
                        break
                    """if dist>=35:
                        R.forward(step=0.5,speed=50)
                        if count<=0:
                            R.right(step=0.15,speed=46)
                            count=6
                        
                    else:
                        ch_index = random.randint(0, 8)
                        print "selected function = ",ch_index
                        choice[ch_index](step=0.9,speed=45)"""
                        
                    count-=1
                    time.sleep(0.05)
                except Exception as e:
                    print'Exception in make move'
                    print e
                    continue
                
                #time.sleep(0.01)
                
        except:
            print "in main except"
            R.reset()
            D.reset()
        finally:
            print "finally closed"
            R.reset()
            D.reset()
    
        
        
    def checkObstacle(self,dl, df, dr):
        global R
        choice = [R.left,R.right,R.left,R.right,R.left,R.right,R.left,R.right]
        if dl < 35:
            print "move right"
            R.right(step = 0.3, speed=45)
        if dr < 35:
            print "move left"
            R.left(step=0.3, speed=45)
        if df < 35:
            ch_index = random.randint(0, len(choice)-1)
            print "move random = ",ch_index
            choice[ch_index](step=0.9,speed=45)
            
        else:
            R.forward(step=0.5, speed=45)
            
        
            
