import io
import os
import socket
import struct
import time
import picamera
import picamera.array
import cv2
import numpy as np
import signal
import sys
import threading
import time
import copy as cp
from Distance import *
from Queue import Queue
from robot import *
from Robot_Canvas import *
from comp import Compass

ip = "localhost"
port = 0
camera = 0
connection=0
client_socket=0
no_connection = False
tstop = Queue(maxsize=10)
t_stream = Queue(maxsize=10)
angle_stream = Queue(maxsize=10)
R = RoboCar()
canvas = Canvas('192.168.100.81',1236)
compass = Compass()
distance = CDistance()

def read_ip():
    global ip,port
    f = open("server_ip.txt", "r")
    ip0 = f.read()
    si = ip0.split(':')
    ip = str(si[0])
    port = int(si[1])
    print 'ip:',ip,'port:',port
def closeAll():
    global camera
    global R
    global connection
    global client_socket
    camera.stop_preview()
    camera.close()
    R.reset()
    #tstop.put(False)
    if connection!=0 and client_socket!=0:
        connection.close()
        client_socket.close()
    return

def signal_handler(signal,frame):
    closeAll()
    print 'all closed;;;;'
    time.sleep(1)
    os._exit(1)


def get_distance():
    global R
    global compass,canvas 
    U_dist = R.sonic_distance()
    return U_dist
    print "sonic distance:",U_dist
    try:
        dist = t_stream.get()
    except:
        dist = U_dist
    print "laser distance:",dist
    
    if dist<=35 and U_dist<=50:
        dist = (dist+U_dist)/2
    elif dist>=35 and U_dist<=50:    
        dist = U_dist
    elif dist<=35 and U_dist>50:    
        dist = dist
    else:
        dist = 100
    return dist

def get_360_readings():
    global R
    global compass,canvas
    
    print 'thread acquired'
    rotate(350,direction='right')
    print '90 degrees calculated'
def getAngleStream():
    try:
        return angle_stream.get()
    except:
        return getAngleStream()
    
def rotate(deg,direction='right'):
    #print 'deg:',deg
    
    global R
    global compass,canvas
    for i in xrange(20):
        angle=getAngleStream()
        #print angle
    #time.sleep(2)
    angle= getAngleStream()

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
        R.right(0.13,speed=30)
        #time.sleep(10)
        for j in xrange(20):
            current_angle = getAngleStream()
            medAngle.append(current_angle)
            #print current_angle
        previous = np.median(medAngle)
        medAngle = []
        current_angle = getAngleStream()
        if abs(previous-current_angle)!=0:
            for j in xrange(20):
                current_angle = getAngleStream()
                medAngle.append(current_angle)
                #print "Again:%d"%current_angle
            current_angle = np.median(medAngle)
        medAngle = []
        print 'target_angle:',target_angle,' current_angle:',current_angle
        try:
            distance=get_distance()
        except:
            print 'Except in sonic'
        print 'distance:',distance
        canvas.update_position(current_angle,distance,rot_bool=True)
        if( abs(current_angle-target_angle)<2):
            break
        
    #if deg==90:
    #    R.right(0.7,speed=30)
    #elif deg==180:
    #    R.right(1.2,speed=30)

def make_move_map():
    global R
    global compass,canvas
    try:
        while True:            
            
            get_360_readings()
            
            break
            """
            try:
                bool_thread = tstop.get()
                
            except:
                print "hello"
                pass
            if bool_thread==False:
                print "me break"
                break"""
    except:
        print "i am in except"
        canvas.write_to_file()
        #break
        sys.exit(0)
    finally:
        canvas.write_to_file()

# Connect a client socket to my_server:8000 (change my_server to the
# hostname of your server)
def program_start():
    global camera
    global connection
    global client_socket
    global no_connection
    global tstop
    global t_stream
    global angle_stream
    read_ip()
    try:
        
        client_socket = socket.socket()
        client_socket.connect((ip, port))
    # Make a file-like object out of the connection
        connection = client_socket.makefile('wb')
    except:
        no_connection = True

    # Make a file-like object out of the connection
    try:
        camera = picamera.PiCamera()
        camera.resolution = (320, 240)
        # Start a preview and let the camera warm up for 2 seconds
        camera.start_preview(fullscreen=False,window=(100,20,320,240))
        time.sleep(1)

        start = time.time()
        stream = io.BytesIO()
        #make_move_map()
        threading.Thread(target=make_move_map).start()
        for foo in camera.capture_continuous(stream, 'jpeg', use_video_port=True,quality=20):
            # Write the length of the capture to the stream and flush to
            # ensure it actually gets sent
            #print 'main'
            data1 = np.fromstring(stream.getvalue(), dtype=np.uint8)
            image1 = cv2.imdecode(data1, 1)
            image1,x_val,y_val,dist = distance.calculate_distance(image1)
            angle=compass.getAngle()
            #_,_,angle=compass.getReadings()
            #print 'angle:',angle
            angle_stream.put(angle,False)
            
            try:
                t_stream.put(dist,False)
            except:
                pass
            if no_connection==False:
                connection.write(struct.pack('<L', stream.tell()))
                connection.flush()
            try:
                tstop.put(True,False)
            except:
                pass
        # Rewind the stream and send the image data over the wire
            if no_connection==False:
                stream.seek(0)
                connection.write(stream.read())
            else:
                stream.seek(0)
                stream.read()
       
            stream.seek(0)
            stream.truncate()
            
    # Write a length of zero to the stream to signal we're done
        if no_connection==False:
            connection.write(struct.pack('<L', 0))
    finally:
        closeAll()
