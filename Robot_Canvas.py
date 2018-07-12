import numpy as np


class Canvas:
    def __init__(self):
        self.rows = 80
        self.cols = 60
        self.array2D = np.ones((self.rows,self.cols),dtype=np.int8)        
        self.current_position = [self.rows/2,self.cols]
        self.direction = "forward"
        self.distance_threshold = 35
        self.step_size = 2.5
        
    def expand_right(self):
        e_cols = np.zeros((self.rows,self.cols/2),dtype=np.int8)
        self.array2D = np.hstack((self.array2D,e_cols))
        self.rows = self.array2D.shape[0]
        self.cols = self.array2D.shape[1]
        
    def expand_left(self):
        e_cols = np.zeros((self.rows,self.cols/2),dtype=np.int8)
        self.array2D = np.hstack((e_cols,self.array2D))
        self.rows = self.array2D.shape[0]
        self.cols = self.array2D.shape[1]
        
    def expand_up(self):
        e_cols = np.zeros((self.rows/2,self.cols),dtype=np.int8)
        self.array2D = np.vstack((e_cols,self.array2D))
        self.rows = self.array2D.shape[0]
        self.cols = self.array2D.shape[1]
        
    def expand_down(self):
        e_cols = np.zeros((self.rows/2,self.cols),dtype=np.int8)
        self.array2D = np.vstack((self.array2D,e_cols))
        self.rows = self.array2D.shape[0]
        self.cols = self.array2D.shape[1]
        
    def check_expension(self):
        if self.direction=="right":
            d = abs(self.current_position[1]-self.cols)
            if d>=13:
                sum= np.sum(self.array2D[self.current_position[0],self.current_position[1]:]==2)
                if sum<1:
                    self.expand_right()
        elif self.direction=="backward":
            d = abs(self.current_position[0]-self.rows)
            if d>=13:
                sum= np.sum(self.array2D[self.current_position[0]:self.rows,self.current_position[1]]==2)
                if sum<1:
                    self.expand_down()        
        elif self.direction=="left":
            if self.current_position[1]<=13:
                sum= np.sum(self.array2D[self.current_position[0],0:self.current_position[1]]==2)
                if sum<1:
                    self.expand_left()            
        elif self.direction=="forward":
            if self.current_position[0]<=13:
                sum= np.sum(self.array2D[0:self.current_position[0],self.current_position[1]]==2)
                if sum<1:
                    self.expand_up()
                    
    def update_position(self,dist):
        self.check_expension()
        dabba = 0
        if dist<=self.distance_threshold:
             dabba = int(dist/self.step_size)
        if self.direction=='forward':
            self.current_position[0]-=1
            self.array2D[self.current_position[0]-dabba,self.current_position[1]] = 2
        elif self.direction=='backward':
            self.current_position[0]+=1
            self.array2D[self.current_position[0]+dabba,self.current_position[1]] = 2
        elif self.direction=='left':
            self.current_position[1]-=1
            self.array2D[self.current_position[0],self.current_position[1]-dabba] = 2
        elif self.direction=='right':
            self.current_position[1]+=1
            self.array2D[self.current_position[0],self.current_position[1]+dabba] = 2
        self.array2D[self.current_position[0],self.current_position[1]] = 1
        

canvas1 = Canvas()
print (canvas1.array2D)
canvas1.expand_right()
print (' ')
print (canvas1.array2D)