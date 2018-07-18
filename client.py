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

ip = "192.168.200.125"
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
def image_show():
    count_range=0
    in_range = False
    dist = 0
    while True:
        try:
            U_dist = R.sonic_distance()
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
            else:
                dist = 100
            print "dist:",dist

            if dist>=35:
                if in_range == False:
                    R.forward(0.1)
                    canvas.update_direction('forward')
                    canvas.update_position()
                #print "out of range"
                if count_range>=10:
                    in_range = False
                    count_range = 0 
                
                if in_range == True:
                    count_range+=1
            else:
                #R.right(1)
                in_range = True
                count_range = 0
                #print "in range"
                canvas.write_to_file()
            canvas.set_obstacle(dist)
    
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
