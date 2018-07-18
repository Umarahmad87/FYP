import RPi.GPIO as gpio
import time

class RoboCar:
    def __init__(self,pin=[29,31,35,37,12,18]):
        try:
            gpio.cleanup()
        finally:
            self.mode = gpio.BOARD
            self.yellow = pin[0]
            self.brown = pin[1]
            self.red  = pin[2]
            self.orange = pin[3]
            self.GPIO_TRIGGER = pin[4]
            self.GPIO_ECHO = pin[5]
            self.setup()
        
    def setup(self):
        gpio.setmode(gpio.BOARD)
        gpio.setup(self.yellow,gpio.OUT)
        gpio.setup(self.brown,gpio.OUT)
        gpio.setup(self.red,gpio.OUT)
        gpio.setup(self.orange,gpio.OUT)
        gpio.setup(self.GPIO_TRIGGER, gpio.OUT)
        gpio.setup(self.GPIO_ECHO, gpio.IN)
        
    def backward(self,step=0):
        gpio.output(self.yellow,False)
        gpio.output(self.brown,True)
        gpio.output(self.red,False)
        gpio.output(self.orange,True)
        if step>0:
            time.sleep(step)
            self.Break()
        #self.left(0.1)
        return
    def forward(self,step=0.0):
        gpio.output(self.yellow,True)
        gpio.output(self.brown,False)
        gpio.output(self.red,True)
        gpio.output(self.orange,False)
        if step>0:
            time.sleep(step)
            self.Break()
        #self.right(0.13)
        return
    def left(self,step=0):
        gpio.output(self.yellow,True)
        gpio.output(self.brown,True)
        gpio.output(self.red,False)
        gpio.output(self.orange,False)
        if step>0:
            time.sleep(step)
            self.Break()
        return
    def right(self,step=0):
        gpio.output(self.yellow,False)
        gpio.output(self.brown,False)
        gpio.output(self.red,True)
        gpio.output(self.orange,True)
        if step>0:
            time.sleep(step)
            self.Break()
        return
    def Break(self):
        gpio.output(self.yellow,False)
        gpio.output(self.brown,False)
        gpio.output(self.red,False)
        gpio.output(self.orange,False)
        return
    def reset(self):
        gpio.cleanup()
        return
    def sonic_distance(self):
        gpio.output(self.GPIO_TRIGGER, True)
 
        time.sleep(0.00001)
        gpio.output(self.GPIO_TRIGGER, False)
 
        StartTime = time.time()
        StopTime = time.time()
        time_check = time.time()
        while gpio.input(self.GPIO_ECHO) == 0:
            StartTime = time.time()
            if StartTime-time_check>=0.05:
                return 200
 
        while gpio.input(self.GPIO_ECHO) == 1:
            StopTime = time.time()
 
        TimeElapsed = StopTime - StartTime
        distance = (TimeElapsed * 34300) / 2
        return distance
