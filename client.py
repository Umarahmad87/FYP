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

ip = "192.168.1.114"
port = 3051
camera = 0
connection=0
client_socket=0

no_connection = False
tstop = Queue(maxsize=1)
t_stream = Queue(maxsize=1)

def closeAll():
    camera.stop_preview()
    camera.close()
    R.reset()
    tstop.put(False) 
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
    while True:
        try:
            st = t_stream.get()
            if st==None:
                #print "none"
                continue
            data1 = np.fromstring(st.getvalue(), dtype=np.uint8)
            image1 = cv2.imdecode(data1, 1)
        
            image1,x_val,y_val,dist = distance.calculate_distance(image1)
            if(dist>=25):
                if in_range == False:
                    R.forward(0.1)
                print "out of range"
                if count_range>=10:
                    in_range = False
                    count_range = 0 
                
                if in_range == True:
                    count_range+=1
            else:
                in_range = True
                count_range = 0
                print "in range"
            bool_thread = tstop.get()
            if bool_thread==False:
                break
        except:
            #print "i am in except"
            continue


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
# Make a file-like object out of the connection
try:
    camera = picamera.PiCamera()
    camera.resolution = (320, 240)
    # Start a preview and let the camera warm up for 2 seconds
    camera.start_preview(fullscreen=False,window=(100,20,320,240))
    time.sleep(1)

    # Note the start time and construct a stream to hold image data
    # temporarily (we could write it directly to connection but in this
    # case we want to find out the size of each capture first to keep
    # our protocol simple)
    start = time.time()    stream = io.BytesIO()
    
    threading.Thread(target=image_show).start()
    for foo in camera.capture_continuous(stream, 'jpeg', use_video_port=True,quality=20):
        # Write the length of the capture to the stream and flush to
        # ensure it actually gets sent
        t_stream.put(stream)
        #print "size=",stream.tell()
        if no_connection==False:
            connection.write(struct.pack('<L', stream.tell()))
            connection.flush()
        tstop.put(True)
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