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

camera = 0
connection=0
client_socket=0



t_Queue = Queue(maxsize=1)
tstop = Queue(maxsize=1)

def closeAll():
    camera.stop_preview()
    camera.close()
    tstop.put(False) 
    connection.close()
    client_socket.close()
    return

def signal_handler(signal,frame):
    closeAll()
    sys.exit(0)


signal.signal(signal.SIGINT,signal_handler)
x= 2
y= 3
stream2 = None
distance = CDistance()
#cv2.namedWindow("Frame")
def image_show():
    while True:
        if stream==None:
            continue
        data1 = np.fromstring(stream.getvalue(), dtype=np.uint8)
        # "Decode" the image from the array, preserving colour
        image1 = cv2.imdecode(data1, 1)
        
        image1,x_val,y_val = distance.calculate_distance(image1)
        
        
        print 'x_s:',x_val,'y_s',y_val
        t_Queue.put((x_val,y_val))
        bool_thread = tstop.get()
        if bool_thread==False:
            break
        try:
            pass
            #image1 = cv2.circle(image1, (320, 240), 1, (255,0,0), 3)
            #image1 = cv2.circle(image1, (int(y_val), int(x_val)), 5, (0,0,255), 3)
            #cv2.imshow("Frame",image1)
        except:
            continue
        
        key2 = cv2.waitKey(5)
        if key2==27:
            closeAll()
            break


# Connect a client socket to my_server:8000 (change my_server to the
# hostname of your server)
client_socket = socket.socket()
client_socket.connect(('192.168.200.102', 2036))
# Make a file-like object out of the connection
connection = client_socket.makefile('wb')
try:
    camera = picamera.PiCamera()
    camera.resolution = (640, 480)
    # Start a preview and let the camera warm up for 2 seconds
    camera.start_preview(fullscreen=False,window=(100,20,640,480))
    time.sleep(2)

    # Note the start time and construct a stream to hold image data
    # temporarily (we could write it directly to connection but in this
    # case we want to find out the size of each capture first to keep
    # our protocol simple)
    start = time.time()
    stream = io.BytesIO()
    
    threading.Thread(target=image_show).start()
    for foo in camera.capture_continuous(stream, 'jpeg', use_video_port=True):
        # Write the length of the capture to the stream and flush to
        # ensure it actually gets sent
        connection.write(struct.pack('<L', stream.tell()))
        connection.flush()
        xy = t_Queue.get()
        tstop.put(True)
        print 'qs:',xy[0],'qy:',xy[1]
        connection.write(struct.pack('<L', xy[0]))
        connection.write(struct.pack('<L', xy[1]))
        
        #stream2 = cp.deepcopy(stream) 
    # Rewind the stream and send the image data over the wire
        stream.seek(0)
        connection.write(stream.read())
        #data = np.fromstring(stream.getvalue(), dtype=np.uint8)
    # "Decode" the image from the array, preserving colour
    #image = cv2.imdecode(data, 1)
    #cv2.imshow("Frame",image)
    # Reset the stream for the next capture
        key = cv2.waitKey(5)
        if key==27: #escape
            closeAll()
            cv2.destroyAllWindows()
            break
        stream.seek(0)
        stream.truncate()
# Write a length of zero to the stream to signal we're done
    connection.write(struct.pack('<L', 0))
finally:
    closeAll()