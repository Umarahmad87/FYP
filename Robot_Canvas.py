import numpy as np


class Canvas:
    def __init__(self):
        self.rows = 80
        self.cols = 60
        self.array2D = np.zeros((self.rows,self.cols),dtype=np.int8)        
        self.current_position = [self.rows/2,self.cols/2]
        self.direction = "forward"
        self.distance_threshold = 35
        self.step_size = 2.5
        
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
        self.rows = self.array2D.shape[0]
        self.cols = self.array2D.shape[1]
        
        
    def expand_up(self):
        e_cols = np.zeros((self.rows/2,self.cols),dtype=np.int8)
        self.array2D = np.vstack((e_cols,self.array2D))
        self.current_position[0]+=self.rows/2
        self.rows = self.array2D.shape[0]
        self.cols = self.array2D.shape[1]
        
        
    def expand_down(self):
        e_cols = np.zeros((self.rows/2,self.cols),dtype=np.int8)
        self.array2D = np.vstack((self.array2D,e_cols))
        self.rows = self.array2D.shape[0]
        self.cols = self.array2D.shape[1]
        #self.current_position[0]-=self.rows/2
        
    def check_expension(self):
        if self.direction=="right":
            d = abs(self.current_position[1]-self.cols)
            if d<=13:
                sum= np.sum(self.array2D[self.current_position[0],self.current_position[1]:]==2)
                if sum<1:
                    self.expand_right()
        elif self.direction=="backward":
            d = abs(self.current_position[0]-self.rows)
            if d<=13:
                sum= np.sum(self.array2D[self.current_position[0]:self.rows,self.current_position[1]]==2)
                if sum<1:
                    self.expand_down()        
        elif self.direction=="left":
            if self.current_position[1]<=13:
                sum= np.sum(self.array2D[self.current_position[0],0:self.current_position[1]]==2)
                if sum<1:
                    self.expand_left()            
        elif self.direction=="forward":
            #print 'forward check'
            if self.current_position[0]<=13:
                sum= np.sum(self.array2D[0:self.current_position[0],self.current_position[1]]==2)
                if sum<1:
                    self.expand_up()
                    
    def update_position(self):
        #print 'current pos:',self.current_position
        try:
            self.check_expension()
        except:
            print 'exception in check expansion'            
        if self.direction=='forward':
            #print 'forward position updated'
            self.current_position[0]-=1
            #print 'subtracted'
            #print 'setteled'
        elif self.direction=='backward':
            self.current_position[0]+=1
        elif self.direction=='left':
            self.current_position[1]-=1
        elif self.direction=='right':
            self.current_position[1]+=1
        print 'Array_size:',self.array2D.shape
        print 'current direction:',self.direction
        print 'current position:',self.current_position[0],':',self.current_position[1]
        self.array2D[self.current_position[0],self.current_position[1]] = 1
         
    
    def update_direction(self,x):
        if x in ['forward','backward','left','right']:
            self.direction = x
    def get_direction(self):
        return self.direction
    def get_next_directions(self):
        if self.direction=='forward':
            return ['right','backward','left','forward']
        if self.direction=='right':
            return ['backward','left','forward','right']
        if self.direction=='backward':
            return ['left','forward','right','backward']
        if self.direction=='left':
            return ['forward','right','backward','left']
        
    def write_to_file(self):
        np.savetxt('array.txt',self.array2D,fmt='%d')
    
    def set_obstacle(self,dist):
        dabba = 0
        if dist<=self.distance_threshold:
             dabba = int(dist/self.step_size)
        if dabba>0:
            if self.direction=='forward':
                self.array2D[self.current_position[0]-dabba,self.current_position[1]] = 2
            elif self.direction=='backward':
                self.array2D[self.current_position[0]+dabba,self.current_position[1]] = 2
            elif self.direction=='left':
                self.array2D[self.current_position[0],self.current_position[1]-dabba] = 2
            elif self.direction=='right':
                self.array2D[self.current_position[0],self.current_position[1]+dabba] = 2
#canvas1 = Canvas()
#print (canvas1.array2D)
#canvas1.expand_right()
#print (' ')
#print (canvas1.array2D)