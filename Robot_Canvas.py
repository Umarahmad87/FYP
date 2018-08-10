import numpy as np
import math

class Canvas:
    def __init__(self):
        self.rows = 80
        self.cols = 60
        self.step_size = 2.5
        self.array2D = np.zeros((self.rows,self.cols),dtype=np.int8)        
        self.current_position = [self.rows/2,self.cols/2]
        self.current_pixels = self.cell_2_pixel(self.current_position[0],self.current_position[1])
        self.direction = "forward"
        self.distance_threshold = 35
    def pixel_2_cell(self,x,y):
        x_ind=int(x/self.step_size)
        y_ind=int(y/self.step_size)
        return x_ind,y_ind
    def cell_2_pixel(self,ind_x,ind_y):
        xpx = int(ind_x*self.step_size)
        ypx = int(ind_y*self.step_size)
        return xpx,ypx
    def angle_2_pixel(self,angle,distance):
        distance*=self.step_size
        print "current pixel: ","(",self.current_pixels[0]," ",self.current_pixels[1],")"
        print "angle: ",angle
        x = distance*round(math.cos(math.radians(angle)),2)+self.current_pixels[0]
        y = distance*round(math.sin(math.radians(angle)),2)+self.current_pixels[1]
        print "calculated x,y: ","(",x," ",y,")"
        return x,y
    def expand_right(self):
        e_cols = np.zeros((self.rows,self.cols/2),dtype=np.int8)
        self.array2D = np.hstack((self.array2D,e_cols))
        self.rows = self.array2D.shape[0]
        self.cols = self.array2D.shape[1]
        #self.current_position[1]-=self.cols/2
        
    def expand_left(self):
        e_cols = np.zeros((self.rows,self.cols/2),dtype=np.int8)
        self.array2D = np.hstack((e_cols,self.array2D))
        self.current_position[1]+=self.cols/2
        self.current_pixels = self.cell_2_pixel(self.current_position[0],self.current_position[1])
        self.rows = self.array2D.shape[0]
        self.cols = self.array2D.shape[1]
        
        
    def expand_up(self):
        e_cols = np.zeros((self.rows/2,self.cols),dtype=np.int8)
        self.array2D = np.vstack((e_cols,self.array2D))
        self.current_position[0]+=self.rows/2
        self.current_pixels = self.cell_2_pixel(self.current_position[0],self.current_position[1])
        self.rows = self.array2D.shape[0]
        self.cols = self.array2D.shape[1]
        
        
    def expand_down(self):
        e_cols = np.zeros((self.rows/2,self.cols),dtype=np.int8)
        self.array2D = np.vstack((self.array2D,e_cols))
        self.rows = self.array2D.shape[0]
        self.cols = self.array2D.shape[1]
        #self.current_position[0]-=self.rows/2
    def set_obstacle(self,dabbax,dabbay,value):
        if (dabbax>=0 and dabbax<self.rows):
            if (dabbay>=0 and dabbay<self.cols):
                self.array2D[dabbax,dabbay] = value
    def check_expension(self,deg,distance):
        h,l = self.angle_2_pixel(deg,distance)
        dabbax,dabbay = self.pixel_2_cell(h,l)
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
        h,l = self.angle_2_pixel(deg,distance)
        dabbax,dabbay = self.pixel_2_cell(h,l)
        print 'dx:',dabbax,'dabbay:',dabbay
        self.set_obstacle(dabbax,dabbay,2)
    def update_position(self,deg,distance,rot_bool=False):
        #print 'current pos:',self.current_position
        try:
            self.check_expension(deg,distance)
        except:
            print 'exception in check expansion'            
        if rot_bool==False:
            dabbax,dabbay = pixel_2_cell(angle_2_pixel(deg,self.step_size))
            self.set_obstacle(dabbax,dabbay,1)
            self.current_position[0] = dabbax
            self.current_position[1] = dabbay
            self.current_pixels = self.cell_2_pixel(self.current_position[0],
                                                    self.current_position[1])
        self.write_to_file()
                 
    def write_to_file(self):
        np.savetxt('array.txt',self.array2D,fmt='%d')
     