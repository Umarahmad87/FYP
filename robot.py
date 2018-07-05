import RPi.GPIO as gpio
import time
import curses

frequency = 90.0
dutycycle = 90.0
stop = 0.0
def set_setup():
    gpio.setmode(gpio.BOARD)
    gpio.setwarnings(False)
    gpio.setup(7,gpio.OUT)
    gpio.setup(11,gpio.OUT)
    gpio.setup(13,gpio.OUT)
    gpio.setup(15,gpio.OUT)
    gpio.setup(16,gpio.OUT)
    gpio.output(16,gpio.HIGH)
    L1 = gpio.PWM(7,frequency)
    L2 = gpio.PWM(11,frequency)
    R1 = gpio.PWM(13,frequency)
    R2 = gpio.PWM(15,frequency)
    L1.start(0)
    L2.start(0)
    R1.start(0)
    R2.start(0)
    return L1,L2,R1,R2

def move_forward(step):
    
    #set_setup()
    #gpio.output(7,False)
    #gpio.output(11,True) #right pane forward
    #gpio.output(13,True) #left pane forward
    #gpio.output(15,False)
    
    L2.ChangeDutyCycle(dutycycle)
    R1.ChangeDutyCycle(dutycycle)
    L1.ChangeDutyCycle(stop)
    R2.ChangeDutyCycle(stop)
    
    #time.sleep(step)
    #gpio.cleanup()
    return

def move_backward(step):
    #set_setup()
    #gpio.output(7,True)
    #gpio.output(11,False)
    #gpio.output(13,False)
    #gpio.output(15,True)
    L1.ChangeDutyCycle(dutycycle)
    R2.ChangeDutyCycle(dutycycle)
    L2.ChangeDutyCycle(stop)
    R1.ChangeDutyCycle(stop)
    #time.sleep(step)
    #gpio.cleanup()
    return

def move_right(step):
    
    L2.ChangeDutyCycle(stop)
    R1.ChangeDutyCycle(dutycycle)
    L1.ChangeDutyCycle(dutycycle)
    R2.ChangeDutyCycle(stop)
    
    
    #set_setup()
    #gpio.output(7,False)
    #gpio.output(11,True) #right pane forward
    #gpio.output(13,False) #left pane forward
    #gpio.output(15,True)
    #time.sleep(step)
    #gpio.cleanup()
    return
def move_left(step):
    
    L2.ChangeDutyCycle(dutycycle)
    R1.ChangeDutyCycle(stop)
    L1.ChangeDutyCycle(stop)
    R2.ChangeDutyCycle(dutycycle)
    
    
    #set_setup()
    #gpio.output(7,True)
    #gpio.output(11,False) #right pane forward
    #gpio.output(13,True) #left pane forward
    #gpio.output(15,False)
    #time.sleep(step)
    #gpio.cleanup()
    return

def Stop():
    L2.ChangeDutyCycle(stop)
    R1.ChangeDutyCycle(stop)
    L1.ChangeDutyCycle(stop)
    R2.ChangeDutyCycle(stop)


def set_speed(Pin,x):
    Pin.ChangeDutyCycle(x)
    return

screen = curses.initscr()
curses.noecho()
curses.cbreak()
screen.keypad(True)

L1,L2,R1,R2 = set_setup()
laserON = True

try:
    while True:
        char = screen.getch()
        if laserON==False:
                gpio.output(16,False)
        elif laserON==True:
            gpio.output(16,True)
        if char==ord('q'):
            break
        if char==ord('z'):
            Stop()
        elif char==curses.KEY_UP:
            move_forward(2)
        elif char==curses.KEY_DOWN:
            move_backward(2)
        elif char==curses.KEY_RIGHT:
            move_right(2)
        elif char==curses.KEY_LEFT:
            move_left(2)
        elif char==ord('s'):
            #set_speed(L1,1)
            #set_speed(L2,1)
            #set_speed(R1,1)
            #set_speed(R2,1)
            #L1.ChangeDutyCycle(100)
            #L2.ChangeDutyCycle(100)
            #R1.ChangeDutyCycle(100)
            #R2.ChangeDutyCycle(100)
            dutycycle+=10
        elif char==ord('a'):
            dutycycle-=10
            #L1.ChangeDutyCycle(0)
            #L2.ChangeDutyCycle(0)
            #R1.ChangeDutyCycle(0)
            #R2.ChangeDutyCycle(0)
        elif char==ord('l'):
            if laserON==True:
                laserON = False
            else:
                laserON = True
    #gpio.cleanup()

finally:
    curses.nocbreak()
    screen.keypad(0)
    curses.echo()
    curses.endwin()
    gpio.cleanup()
    print ('HELLO')