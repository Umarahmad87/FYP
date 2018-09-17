import socket
import json
import socket
import json
import numpy as np
from scipy.misc import imsave
import ast
import pandas as pd


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('192.168.100.81', 1236))
s.listen(1)
conn, addr = s.accept()
b = b''
print 'connected'
k = 1
while 1:
    tmp = conn.recv(1024)
    s = ast.literal_eval(tmp)
    print s
    K = np.zeros(tuple(s["size"]),dtype='int16')
    data = pd.DataFrame(s["2"],columns=['row','col'],dtype='int16')
    K[[data['row'].values],[data['col'].values]] =255
    imsave('map'+str(k)+'.png',K)
    k+=1
    b += tmp
d = json.loads(b.decode('utf-8'))
