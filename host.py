import io
import socket
import struct
import cv2
import numpy as np
import threading

# Start a socket listening for connections on 0.0.0.0:8000 (0.0.0.0 means
# all interfaces)

server_socket2 = socket.socket()
server_socket2.bind(('192.168.1.114', 3048))
print 'binded2'
server_socket2.listen(0)


def read_xy():
    connection2 = server_socket2.accept()[0].makefile('rb')
    while True:
        try: 
            xc = struct.unpack('<L', connection2.read(struct.calcsize('<L')))[0]
            yc = struct.unpack('<L', connection2.read(struct.calcsize('<L')))[0]
            print 'x:',xc,'y:',yc
        except:
            print 'except'
            continue       
threading.Thread(target=read_xy).start()

server_socket = socket.socket()
server_socket.bind(('192.168.1.114', 3047))
print 'binded1'
server_socket.listen(0)


# Accept a single connection and make a file-like object out of it
connection = server_socket.accept()[0].makefile('rb')
try:
    while True:
        # Read the length of the image as a 32-bit unsigned int. If the
        # length is zero, quit the loop
        image_len = struct.unpack('<L', connection.read(struct.calcsize('<L')))[0]
        if not image_len:
            break
        #xc = struct.unpack('<L', connection.read(struct.calcsize('<L')))[0]
        #yc = struct.unpack('<L', connection.read(struct.calcsize('<L')))[0]
        #print 'x:',xc,'y:',yc
        # Construct a stream to hold the image data and read the image
        # data from the connection
        image_stream = io.BytesIO()
        image_stream.write(connection.read(image_len))
        # Rewind the stream, open it as an image with opencv and do some
        # processing on it
        image_stream.seek(0)
        #image = Image.open(image_stream)

        print 'Image Read'

        #xc = struct.unpack('<L', connection.read(struct.calcsize('<L')))[0]
        #yc = struct.unpack('<L', connection.read(struct.calcsize('<L')))[0]
        #print 'x:',xc,'y:',yc
        


        data = np.fromstring(image_stream.getvalue(), dtype=np.uint8)
        imagedisp = cv2.imdecode(data, 1)
        imagedisp = cv2.circle(imagedisp,(int(320),int(240)),2,(255,0,0),2)
        #imagedisp = cv2.circle(imagedisp,(int(yc),int(xc)),5,(0,0,255),3)   
        cv2.imshow("Frame",imagedisp)
        #cv2.waitKey(1)  #imshow will not output an image if you do not use waitKey
        #cv2.destroyAllWindows() #cleanup windows
        key = cv2.waitKey(20)
        if key==27:
            cv2.destroyAllWindows()
            break
finally:
    connection.close()
    server_socket.close()
    connection2.close()
    server_socket2.close()