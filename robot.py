import RPi.GPIO as gpio
import time

class RoboCar:
    def __init__(self,pin=[29,31,35,37,12,18]):
        try:
            gpio.cleanup()
        finally:
            self.mode = gpio.BOARD
            #self.yellow = pin[0]
            #self.brown = pin[1]
            #self.red  = pin[2]
            #self.orange = pin[3]
            
            self.L1 = pin[0] # yellow
            self.L2 = pin[3] # orange
            self.R1 = pin[2] # red
            self.R2 = pin[1] # brown
            
            self.p=0
            self.q=0
            self.a=0
            self.b=0
        
            self.GPIO_TRIGGER = pin[4]
            self.GPIO_ECHO = pin[5]
            self.setup()
            
            
        
    def setup(self):
        """gpio.setmode(gpio.BOARD)
        gpio.setup(self.yellow,gpio.OUT)
        gpio.setup(self.brown,gpio.OUT)
        gpio.setup(self.red,gpio.OUT)
        gpio.setup(self.orange,gpio.OUT)"""
        
        gpio.setmode(self.mode)
        gpio.setup(self.GPIO_TRIGGER, gpio.OUT)
        gpio.setup(self.GPIO_ECHO, gpio.IN)
        
        
        #use pwm on inputs so motors don't go too fast
        gpio.setup(self.L1, gpio.OUT)
        self.p = gpio.PWM(self.L1, 20)
        self.p.start(0)

        gpio.setup(self.L2, gpio.OUT)
        self.q = gpio.PWM(self.L2, 20)
        self.q.start(0)

        gpio.setup(self.R1, gpio.OUT)
        self.a = gpio.PWM(self.R1, 20)
        self.a.start(0)

        gpio.setup(self.R2, gpio.OUT)
        self.b = gpio.PWM(self.R2, 20)
        self.b.start(0)

        
    def backward(self,step=0,speed=10):
        #gpio.output(self.yellow,False)
        #gpio.output(self.brown,True)
        #gpio.output(self.red,False)
        #gpio.output(self.orange,True)
        
        self.p.ChangeDutyCycle(0)
        self.q.ChangeDutyCycle(speed)
        self.a.ChangeDutyCycle(0)
        self.b.ChangeDutyCycle(speed)
        #q.ChangeFrequency(speed + 5)
        #b.ChangeFrequency(speed + 5)
        if step>0:
            time.sleep(step)
            self.Break()
        #self.left(0.1)
        return
    def forward(self,step=0.0,speed=10):
        #gpio.output(self.yellow,True)
        #gpio.output(self.brown,False)
        #gpio.output(self.red,True)
        self.p.ChangeDutyCycle(speed)
        self.q.ChangeDutyCycle(0)
        self.a.ChangeDutyCycle(speed)
        self.b.ChangeDutyCycle(0)
        #p.ChangeFrequency(speed + 5)
        #a.ChangeFrequency(speed + 5)#gpio.output(self.orange,False)
            
        if step>0:
            time.sleep(step)
            self.Break()
        #self.right(0.13)
        return
    def left(self,step=0,speed=10):
        #gpio.output(self.yellow,True)
        #gpio.output(self.brown,True)
        #gpio.output(self.red,False)
        #gpio.output(self.orange,False)
        
        self.p.ChangeDutyCycle(speed)
        self.q.ChangeDutyCycle(0)
        self.a.ChangeDutyCycle(0)
        self.b.ChangeDutyCycle(speed)
        #p.ChangeFrequency(speed + 5)
        #b.ChangeFrequency(speed + 5)
        if step>0:
            time.sleep(step)
            self.Break()
        return
    def right(self,step=0,speed=10):
        #gpio.output(self.yellow,False)
        #gpio.output(self.brown,False)
        #gpio.output(self.red,True)
        #gpio.output(self.orange,True)
        
        self.p.ChangeDutyCycle(0)
        self.q.ChangeDutyCycle(speed)
        self.a.ChangeDutyCycle(speed)
        self.b.ChangeDutyCycle(0)
        #q.ChangeFrequency(speed + 5)
        #a.ChangeFrequency(speed + 5)
        
        if step>0:
            time.sleep(step)
            self.Break()
        return
    def Break(self):
        self.p.ChangeDutyCycle(0)
        self.q.ChangeDutyCycle(0)
        self.a.ChangeDutyCycle(0)
        self.b.ChangeDutyCycle(0)
        #gpio.output(self.yellow,False)
        #gpio.output(self.brown,False)
        #gpio.output(self.red,False)
        #gpio.output(self.orange,False)
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
            #if StartTime-time_check>=0.05:
            #    return 200
 
        while gpio.input(self.GPIO_ECHO) == 1:
            StopTime = time.time()
 
        TimeElapsed = StopTime - StartTime
        distance = (TimeElapsed * 34300) / 2
        return distance
