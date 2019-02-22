

import numpy as np
import os
import six.moves.urllib as urllib
import sys
import tarfile
import tensorflow as tf
import zipfile

from collections import defaultdict
from io import StringIO
from matplotlib import pyplot as plt
from PIL import Image
import time

from utils import label_map_util

from utils import visualization_utils as vis_util


import io
import socket
import struct
import threading
from Queue import Queue

t_queue = Queue()
# Start a socket listening for connections on 0.0.0.0:8000 (0.0.0.0 means
# all interfaces)



# # Model preparation 
# Any model exported using the `export_inference_graph.py` tool can be loaded here simply by changing `PATH_TO_CKPT` to point to a new .pb file.  
# By default we use an "SSD with Mobilenet" model here. See the [detection model zoo](https://github.com/tensorflow/models/blob/master/object_detection/g3doc/detection_model_zoo.md) for a list of other models that can be run out-of-the-box with varying speeds and accuracies.

# What model to download.
MODEL_NAME = 'ssd_mobilenet_v1_coco_11_06_2017'
MODEL_FILE = MODEL_NAME + '.tar.gz'
DOWNLOAD_BASE = 'http://download.tensorflow.org/models/object_detection/'

# Path to frozen detection graph. This is the actual model that is used for the object detection.
PATH_TO_CKPT = MODEL_NAME + '/frozen_inference_graph.pb'

# List of the strings that is used to add correct label for each box.
PATH_TO_LABELS = os.path.join('data', 'mscoco_label_map.pbtxt')

NUM_CLASSES = 90


# ## Download Model

if not os.path.exists(MODEL_NAME + '/frozen_inference_graph.pb'):
	print ('Downloading the model')
	opener = urllib.request.URLopener()
	opener.retrieve(DOWNLOAD_BASE + MODEL_FILE, MODEL_FILE)
	tar_file = tarfile.open(MODEL_FILE)
	for file in tar_file.getmembers():
	  file_name = os.path.basename(file.name)
	  if 'frozen_inference_graph.pb' in file_name:
	    tar_file.extract(file, os.getcwd())
	print ('Download complete')
else:
	print ('Model already exists')

# ## Load a (frozen) Tensorflow model into memory.


#intializing the web camera device

import cv2

detection_graph = tf.Graph()
with detection_graph.as_default():
  od_graph_def = tf.GraphDef()
  with tf.gfile.GFile(PATH_TO_CKPT, 'rb') as fid:
    serialized_graph = fid.read()
    od_graph_def.ParseFromString(serialized_graph)
    tf.import_graph_def(od_graph_def, name='')


# ## Loading label map
# Label maps map indices to category names, so that when our convolution network predicts `5`, we know that this corresponds to `airplane`.  Here we use internal utility functions, but anything that returns a dictionary mapping integers to appropriate string labels would be fine

label_map = label_map_util.load_labelmap(PATH_TO_LABELS)
categories = label_map_util.convert_label_map_to_categories(label_map, max_num_classes=NUM_CLASSES, use_display_name=True)
category_index = label_map_util.create_category_index(categories)



'''
def object_detect():
	global t_queue
	#cap = cv2.VideoCapture(0)
	detection_graph = tf.Graph()
	with detection_graph.as_default():
	  od_graph_def = tf.GraphDef()
	  with tf.gfile.GFile(PATH_TO_CKPT, 'rb') as fid:
	    serialized_graph = fid.read()
	    od_graph_def.ParseFromString(serialized_graph)
	    tf.import_graph_def(od_graph_def, name='')


	# ## Loading label map
	# Label maps map indices to category names, so that when our convolution network predicts `5`, we know that this corresponds to `airplane`.  Here we use internal utility functions, but anything that returns a dictionary mapping integers to appropriate string labels would be fine

	label_map = label_map_util.load_labelmap(PATH_TO_LABELS)
	categories = label_map_util.convert_label_map_to_categories(label_map, max_num_classes=NUM_CLASSES, use_display_name=True)
	category_index = label_map_util.create_category_index(categories)


	# Running the tensorflow session
	with detection_graph.as_default():
	  with tf.Session(graph=detection_graph) as sess:
	   ret = True
	   while (ret):
	      #ret,image_np = cap.read()
	      try:
	      	image_np = t_queue.get()
              except:
		print 'in continue'
		continue
	      # Expand dimensions since the model expects images to have shape: [1, None, None, 3]
	      image_np_expanded = np.expand_dims(image_np, axis=0)
	      image_tensor = detection_graph.get_tensor_by_name('image_tensor:0')
	      # Each box represents a part of the image where a particular object was detected.
	      boxes = detection_graph.get_tensor_by_name('detection_boxes:0')
	      # Each score represent how level of confidence for each of the objects.
	      # Score is shown on the result image, together with the class label.
	      scores = detection_graph.get_tensor_by_name('detection_scores:0')
	      classes = detection_graph.get_tensor_by_name('detection_classes:0')
	      num_detections = detection_graph.get_tensor_by_name('num_detections:0')
	      # Actual detection.
	      (boxes, scores, classes, num_detections) = sess.run(
		  [boxes, scores, classes, num_detections],
		  feed_dict={image_tensor: image_np_expanded})
	      # Visualization of the results of a detection.
	      vis_util.visualize_boxes_and_labels_on_image_array(
		  image_np,
		  np.squeeze(boxes),
		  np.squeeze(classes).astype(np.int32),
		  np.squeeze(scores),
		  category_index,
		  use_normalized_coordinates=True,
		  line_thickness=8)
	#      plt.figure(figsize=IMAGE_SIZE)
	#      plt.imshow(image_np)
	      cv2.imshow('image',cv2.resize(image_np,(640,480)))
	      if cv2.waitKey(25) & 0xFF == ord('q'):
		  cv2.destroyAllWindows()
		  #cap.release()
		  break
'''
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('output1122.avi',fourcc, 30.0, (640,480))
server_socket = socket.socket()
server_socket.bind(('192.168.0.193', 3051))
print 'binded1'
server_socket.listen(0)
print 'connected'
boolCount = True
count = 0
# Accept a single connection and make a file-like object out of it
connection = server_socket.accept()[0].makefile('rb')
server_socket._sock.setblocking(0)
#threading.Thread(target=object_detect).start()
try:
  with detection_graph.as_default():
    with tf.Session(graph=detection_graph) as sess:
	    time.sleep(0.5)
	    while True:
		# Read the length of the image as a 32-bit unsigned int. If the
		# length is zero, quit the loop
		image_len = struct.unpack('<L', connection.read(struct.calcsize('<L')))[0]
		#print image_len
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
		    #print 'Image Read'


		    data = np.fromstring(image_stream.getvalue(), dtype=np.uint8)
		    imagedisp = cv2.imdecode(data, 1)
		    #imagedisp = cv2.circle(imagedisp,(int(320),int(240)),2,(255,0,0),2)
		    #imagedisp = cv2.circle(imagedisp,(int(yc),int(xc)),5,(0,0,255),3)   
		    if boolCount==True:
		        t_queue.put(imagedisp,False)
		    else:
			image_np = t_queue.get()
		        image_np_expanded = np.expand_dims(image_np, axis=0)
		        image_tensor = detection_graph.get_tensor_by_name('image_tensor:0')
		        # Each box represents a part of the image where a particular object was detected.
		        boxes = detection_graph.get_tensor_by_name('detection_boxes:0')
		        # Each score represent how level of confidence for each of the objects.
		        # Score is shown on the result image, together with the class label.
		        scores = detection_graph.get_tensor_by_name('detection_scores:0')
		        classes = detection_graph.get_tensor_by_name('detection_classes:0')
		        num_detections = detection_graph.get_tensor_by_name('num_detections:0')
		        # Actual detection.
		        (boxes, scores, classes, num_detections) = sess.run(
			    [boxes, scores, classes, num_detections],
			    feed_dict={image_tensor: image_np_expanded})
		        # Visualization of the results of a detection.
		        vis_util.visualize_boxes_and_labels_on_image_array(
			    image_np,
			    np.squeeze(boxes),
			    np.squeeze(classes).astype(np.int32),
			    np.squeeze(scores),
			    category_index,
			    use_normalized_coordinates=True,
			    line_thickness=8)
		#        plt.figure(figsize=IMAGE_SIZE)
		#        plt.imshow(image_np)
		        cv2.imshow('image',cv2.resize(image_np,(640,480)))

		        #cv2.imshow("Frame",t_queue.get(False))
                        out.write(cv2.resize(image_np,(640,480)))
		        t_queue.put(imagedisp,False)
		    #cv2.waitKey(1)  #imshow will not output an image if you do not use waitKey
		    #cv2.destroyAllWindows() #cleanup windows
		    key = cv2.waitKey(20)
		    if key==27:
                        out.release()
		        cv2.destroyAllWindows()
		        break
		    if count>=5:
		        count=0
		        boolCount=False
		    count+=1
		else:
                    imgttq = t_queue.get(False)
		    cv2.imshow("Frame",imgttq)
finally:
    out.release()
    connection.close()
    server_socket.close()
    #connection2.close()
    #server_socket2.close()

