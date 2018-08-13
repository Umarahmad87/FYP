
import io
import socket
import struct
import cv2
import numpy as np
import threading
from Queue import Queue

# Start a socket listening for connections on 0.0.0.0:8000 (0.0.0.0 means
# all interfaces)

t_queue = Queue()
server_socket = socket.socket()
server_socket.bind(('192.168.200.103', 3051))
print 'binded1'
server_socket.listen(0)
boolCount = True
count = 0
# Accept a single connection and make a file-like object out of it
connection = server_socket.accept()[0].makefile('rb')
server_socket._sock.setblocking(0)
try:
    while True:
        # Read the length of the image as a 32-bit unsigned int. If the
        # length is zero, quit the loop
        image_len = struct.unpack('<L', connection.read(struct.calcsize('<L')))[0]
        print image_len
        if image_len!=None:
            if not image_len:
                break
            # Construct a stream to hold the image data and read the image
            # data from the connection
            image_stream = io.BytesIO()
            image_stream.write(connection.read(image_len))
            # Rewind the stream, open it as an image with opencv and do some
            # processing on it
            image_stream.seek(0)
            print 'Image Read'


            data = np.fromstring(image_stream.getvalue(), dtype=np.uint8)
            imagedisp = cv2.imdecode(data, 1)
            imagedisp = cv2.circle(imagedisp,(int(320),int(240)),2,(255,0,0),2)
            #imagedisp = cv2.circle(imagedisp,(int(yc),int(xc)),5,(0,0,255),3)   
            if boolCount==True:
                t_queue.put(imagedisp,False)
            else:
                cv2.imshow("Frame",t_queue.get(False))
                t_queue.put(imagedisp,False)
            #cv2.waitKey(1)  #imshow will not output an image if you do not use waitKey
            #cv2.destroyAllWindows() #cleanup windows
            key = cv2.waitKey(20)
            if key==27:
                cv2.destroyAllWindows()
                break
            if count>=5:
                count=0
                boolCount=False
            count+=1
        else:
            cv2.imshow("Frame",t_queue.get(False))
finally:
    connection.close()
    server_socket.close()
    #connection2.close()
    #server_socket2.close()