import numpy as np
import math
import io
import socket
import json
from collections import defaultdict
import sets

class Canvas:
    def __init__(self,ip,port):
        self.map_dict = defaultdict(lambda:[])
        self.map_dict[1] = []
        self.map_dict[2] = []
        self.rows = 1800
        self.cols = 1600
        self.step_size = 4#4
        self.car_distance = 2
        self.boxCount = self.car_distance
        #self.array2D = np.zeros((self.rows,self.cols),dtype=np.int8)        
        self.current_position = [self.rows/2,self.cols/2]
        self.current_pixels = self.cell_2_pixel(self.current_position[0],self.current_position[1])
        self.direction = "forward"
        self.distance_threshold = 35
        self.set_obstacle( self.current_position[0], self.current_position[1],1)
        self.no_connection = False
        self.client_socket = 0
        try:
        
            self.client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            self.client_socket.settimeout(5)
            self.client_socket.connect((ip, port))
            print 'Canvas connected to Server'
        # Make a file-like object out of the connection
        except:
            self.no_connection = True
            print 'Canvas not connected to Server'
        
    def pixel_2_cell(self,x,y):
        x_ind=int(x/self.step_size)
        y_ind=int(y/self.step_size)
        return x_ind,y_ind
    def cell_2_pixel(self,ind_x,ind_y):
        xpx = int(ind_x*self.step_size)
        ypx = int(ind_y*self.step_size)
        return xpx,ypx
    def angle_2_pixel(self,angle,distance):
        distance/=self.step_size
        #print "current pixel: ","(",self.current_pixels[0]," ",self.current_pixels[1],")"
        #print "angle: ",angle
        x = distance*round(math.cos(math.radians(angle)),2)+self.current_position[0]
        y = distance*round(math.sin(math.radians(angle)),2)+self.current_position[1]
        #print "calculated x,y: ","(",x," ",y,")"
        return int(x),int(y)
    def expand_right(self):
        #e_cols = np.zeros((self.rows,self.cols/2),dtype=np.int8)
        #self.array2D = np.hstack((self.array2D,e_cols))
        #self.rows = self.array2D.shape[0]
        #self.cols = self.array2D.shape[1]
        #self.current_position[1]-=self.cols/2
        self.rows = self.rows
        self.cols = self.cols + self.cols/2
        
        
    def expand_left(self):
        #e_cols = np.zeros((self.rows,self.cols/2),dtype=np.int8)
        #self.array2D = np.hstack((e_cols,self.array2D))
        self.current_position[1]+=self.cols/2
        self.current_pixels = self.cell_2_pixel(self.current_position[0],self.current_position[1])
        #self.rows = self.array2D.shape[0]
        #self.cols = self.array2D.shape[1]
        self.rows = self.rows
        self.cols = self.cols + self.cols/2
        
    def expand_up(self):
        
        self.current_position[0]+=self.rows/2
        self.current_pixels = self.cell_2_pixel(self.current_position[0],self.current_position[1])
        
        self.rows = (self.rows/2)+self.rows
        self.cols = self.cols
        
        
    def expand_down(self):
        
        self.rows = (self.rows/2)+self.rows
        self.cols = self.cols
        
    def set_obstacle(self,dabbax,dabbay,value):
        if (dabbax>=0 and dabbax<self.rows):
            if (dabbay>=0 and dabbay<self.cols):
                #self.array2D[dabbax,dabbay] = value
                dabbas = self.map_dict[value]
                dabbas.append([dabbax,dabbay])
                #dabbas = sets.Set(dabbas)
                dabbas = set(tuple(i) for i in dabbas)
                dabbas = [list(i) for i in dabbas]
                    
                print dabbas
                self.map_dict[value] = dabbas
    def check_expension(self,deg,distance):
        if distance<=100:
            dabbax,dabbay = self.angle_2_pixel(deg,distance)
            print 'dx1:',dabbax,'dabbay1:',dabbay
            if deg >=45 and deg<=135:
                if dabbay>=self.cols:
                    self.expand_right()
            elif deg >=135 and deg<=225:
                if dabbax<=1:
                    self.expand_up()
            elif deg >=225 and deg<=315:
                if dabbay<=1:
                    self.expand_left()
            elif deg >=315 and deg<=45:
                if dabbax>=self.rows:
                    self.expand_down()
            dabbax,dabbay = self.angle_2_pixel(deg,distance)
            print 'dx:',dabbax,'dabbay:',dabbay
            self.set_obstacle(dabbax,dabbay,2)
        
    def update_position(self,deg,distance,rot_bool=False):
        
        try:
            self.check_expension(deg[0],distance[0])
            self.check_expension(deg[1],distance[1])
            self.check_expension(deg[2],distance[2])
        except:
            print 'exception in check expansion'            
        if rot_bool==False:
            dabbax,dabbay = self.angle_2_pixel(deg,self.boxCount)
            self.set_obstacle(dabbax,dabbay,1)
            #print 'rot_false'
            if dabbax == self.current_position[0] and dabbay == self.current_position[1]:
                self.boxCount+=self.car_distance
            else:
                self.boxCount=self.car_distance
            self.current_position[0] = dabbax
#            self.current_position[1] = dabbay
            self.current_pixels = self.cell_2_pixel(self.current_position[0],
                                                    self.current_position[1])
        #print 'writing file'
        self.map_dict['pos'] = self.current_position
        self.map_dict['size'] = [self.rows,self.cols]
        self.write_to_file()
        #print 'writing file 2'
    def close_connection(self):
        self.client_socket.close()
    def write_to_file(self):
        #np.savetxt('array.txt',self.array2D,fmt='%d')
        #print 'self.map_dict',self.map_dict
        if self.no_connection==False:
            b = json.dumps(self.map_dict).encode('utf-8')
            self.client_socket.sendall(b)
     