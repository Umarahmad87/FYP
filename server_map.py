import socket
import json
import socket
import json
import numpy as np
from scipy.misc import imsave
import ast
import pandas as pd
import cv2

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('192.168.0.193', 1215))
s.listen(1)
conn, addr = s.accept()
b = b''
print 'connected'
k = 1
kernel = np.ones((2,6),np.float32)#/31
kernel2 = np.ones((3,3), np.uint8)
while 1:
    tmp = conn.recv(1024)
    s = ast.literal_eval(tmp)
    print s
    if(len(s["2"])==0):
        s["2"] = s["1"]
    if(len(s["3"])==0):
        s["3"] = s["1"] 	
    data = pd.DataFrame(s["2"],columns=['row','col'],dtype='int16')
    data2 = pd.DataFrame(s["1"],columns=['row','col'],dtype='int16')
    data3 = pd.DataFrame(s["3"],columns=['row','col'],dtype='int16')
    maxrow = int(max([data['row'].max(),data2['row'].max(),data3['row'].max()]))
    maxcol = int(max([data['col'].max(),data2['col'].max(),data3['col'].max()]))
    minrow = int(min([data['row'].min(),data2['row'].min(),data3['row'].min()]))
    mincol = int(min([data['col'].min(),data2['col'].min(),data3['col'].min()]))
    print "maxrow :",maxrow," minrow :",minrow
    print "maxcol :",maxcol," mincol :",mincol
    K = np.zeros((maxrow+20,maxcol+20,3),dtype='int16') # maxrow+20
    K[[data['row'].values],[data['col'].values]] =[255,0,0]
    K[[data3['row'].values],[data3['col'].values]] =[128,255,128]
    K[[data2['row'].values],[data2['col'].values]] =[0,0,255]
    RA = K[minrow:maxrow+1,mincol:maxcol+1,:]	
    
    #print 'hhhh'
    img_dilation = cv2.dilate(RA, kernel2, iterations=1)
    dst = cv2.filter2D(RA,-1,kernel,(100,9))
    #print 'hhhh2222'
    
    imsave('map.png',img_dilation)
    k+=1
    b += tmp
    #print 'hhhh333'
    
d = json.loads(b.decode('utf-8'))
