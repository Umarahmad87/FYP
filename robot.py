import RPi.GPIO as gpio
import time

class RoboCar:
    def __init__(self,pin=[29,31,35,37]):
        try:
            gpio.cleanup()
        finally:
            self.mode = gpio.BOARD
            self.yellow = pin[0]
            self.brown = pin[1]
            self.red  = pin[2]
            self.orange = pin[3]
            self.setup()
        
    def setup(self):
        gpio.setmode(gpio.BOARD)
        gpio.setup(self.yellow,gpio.OUT)
        gpio.setup(self.brown,gpio.OUT)
        gpio.setup(self.red,gpio.OUT)
        gpio.setup(self.orange,gpio.OUT)
        
    def forward(self,step=0):
        gpio.output(self.yellow,False)
        gpio.output(self.brown,False)
        gpio.output(self.red,True)
        gpio.output(self.orange,True)
        if step>0:
            time.sleep(step)
            self.Break()
        return
    def backward(self,step=0):
        gpio.output(self.yellow,True)
        gpio.output(self.brown,True)
        gpio.output(self.red,False)
        gpio.output(self.orange,False)
        if step>0:
            time.sleep(step)
            self.Break()
        return
    def left(self,step=0):
        gpio.output(self.yellow,False)
        gpio.output(self.brown,True)
        gpio.output(self.red,False)
        gpio.output(self.orange,True)
        if step>0:
            time.sleep(step)
            self.Break()
        return
    def right(self,step=0):
        gpio.output(self.yellow,True)
        gpio.output(self.brown,False)
        gpio.output(self.red,True)
        gpio.output(self.orange,False)
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