import io
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

ip = "192.168.10.125"
port = 3051
camera = 0
connection=0
client_socket=0

no_connection = False
tstop = Queue(maxsize=10)
t_stream = Queue(maxsize=10)

def closeAll():
    camera.stop_preview()
    camera.close()
    R.reset()
    #tstop.put(False) 
    connection.close()
    client_socket.close()
    return

def signal_handler(signal,frame):
    closeAll()
    sys.exit(0)

signal.signal(signal.SIGINT,signal_handler)
distance = CDistance()

def get_distance():
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
    #positions = ['right','backward','left','forward']
    positions = canvas.get_next_directions()
    print '360'
    dista360 = []
    for pos in positions:
        move_right(90)
        #R.right(0.6,speed=30)
        canvas.update_direction(pos)

        dist = get_distance()
        dista360.append(dist)
        print "dist:",dist
        
        time.sleep(0.5)
        
        canvas.set_obstacle(dist)
    return dista360,positions

def move_right(deg):
    if deg==90:
        R.right(0.7,speed=30)
    elif deg==180:
        R.right(1.2,speed=30)

def rotate_to_direction(direction1):
    c_dir = canvas.get_direction()
    print 'direction to move:',direction1
    print 'current direction:',c_dir
    canvas.update_direction(direction1)
    directions = ['forward','backward','right','left']
    Move_Matrix = [  [(0,0,0),(90,90,0),(90,0,0),(90,90,90)], [(90,90,0),(0,0,0),(90,90,90),(90,0,0)], [(90,90,90),(90,0,0),(0,0,0),(90,90,0)], [(90,0,0),(90,90,90),(90,90,0),(0,0,0)]]
    rr=directions.index(c_dir)
    cc=directions.index(direction1)
    moves=Move_Matrix[rr][cc]
    print 'moves:',moves
    move_right(moves[0])
    move_right(moves[1])
    move_right(moves[2])

def image_show():
    count_range=0
    in_range = False
    dist = 0
    positions = ['right','backward','left','forward']
    bool1 = True
    while True:
        try:
             
            if bool1==True:
                dists,positiona = get_360_readings()
                dir_to_move = positiona[np.argmax(dists)]
                rotate_to_direction(dir_to_move)
                print 'moving to:',dir_to_move
                #canvas.update_position()
                canvas.write_to_file()    
                bool1=False
                print 'sleep'
                time.sleep(1)
                print 'awake from sleep'
            
            print 'forward'
            R.forward(0.3,speed=30)
            try:
                canvas.update_position()
            except:
                print 'exception in canvas update position'
        
            dist = get_distance()
            print 'dist:',dist
        
            if dist<=35:
                bool1=True
                #print 'break break break'
                #break
            
            #if dist>=35:
            #    if in_range == False:
            #        R.forward(0.1)
            #        canvas.update_direction('forward')
            #        canvas.update_position()
                #print "out of range"
            #    if count_range>=10:
            #        in_range = False
            #        count_range = 0 
                
            #    if in_range == True:
            #        count_range+=1
            #else:
            #    R.right(2)
            #    in_range = True
            #    count_range = 0
                #print "in range"
            #    canvas.write_to_file()
            
    
            try:
                bool_thread = tstop.get()
                
            except:
                print "hello"
                pass
            if bool_thread==False:
                print "me break"
                break
        except:
            print "i am in except"
            canvas.write_to_file()
            #break
            sys.exit(0)
        finally:
            canvas.write_to_file()

# Connect a client socket to my_server:8000 (change my_server to the
# hostname of your server)
try:
    
    client_socket = socket.socket()
    client_socket.connect((ip, port))
# Make a file-like object out of the connection
    connection = client_socket.makefile('wb')
except:
    no_connection = True
R = RoboCar()
canvas = Canvas()
# Make a file-like object out of the connection
try:
    camera = picamera.PiCamera()
    camera.resolution = (320, 240)
    # Start a preview and let the camera warm up for 2 seconds
    camera.start_preview(fullscreen=False,window=(100,20,320,240))
    time.sleep(1)

    start = time.time()
    stream = io.BytesIO()
    
    threading.Thread(target=image_show).start()
    for foo in camera.capture_continuous(stream, 'jpeg', use_video_port=True,quality=20):
        # Write the length of the capture to the stream and flush to
        # ensure it actually gets sent
        data1 = np.fromstring(stream.getvalue(), dtype=np.uint8)
        image1 = cv2.imdecode(data1, 1)
        image1,x_val,y_val,dist = distance.calculate_distance(image1)
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
