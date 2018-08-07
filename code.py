import RPi.GPIO as GPIO, sys, threading, time, os,curses

GPIO.setwarnings(False) # Pah, who needs runtime errors nowadays?! MTB edit

# Pins 24, 26 Left Motor
# Pins 19, 21 Right Motor
L1 = 29
L2 = 37
R1 = 35
R2 = 31

pwmMax = 4095 # maximum PWM value

#======================================================================
# General Functions
#
# init(). Initialises GPIO pins, switches motors and LEDs Off, etc
def init():
    global p, q, a, b
    GPIO.setmode(GPIO.BOARD)
    #use pwm on inputs so motors don't go too fast
    GPIO.setup(L1, GPIO.OUT)
    p = GPIO.PWM(L1, 20)
    p.start(0)

    GPIO.setup(L2, GPIO.OUT)
    q = GPIO.PWM(L2, 20)
    q.start(0)

    GPIO.setup(R1, GPIO.OUT)
    a = GPIO.PWM(R1, 20)
    a.start(0)

    GPIO.setup(R2, GPIO.OUT)
    b = GPIO.PWM(R2, 20)
    b.start(0)


# cleanup(). Sets all motors and LEDs off and sets GPIO to standard values

def cleanup():
    stop()
    GPIO.cleanup()


# End of General Functions
#======================================================================


#======================================================================
# Motor Functions
# (both versions)
#
# stop(): Stops both motors
def stop():
    p.ChangeDutyCycle(0)
    q.ChangeDutyCycle(0)
    a.ChangeDutyCycle(0)
    b.ChangeDutyCycle(0)
    
# forward(speed): Sets both motors to move forward at speed. 0 <= speed <= 100
def forward(speed):
    p.ChangeDutyCycle(speed)
    q.ChangeDutyCycle(0)
    a.ChangeDutyCycle(speed)
    b.ChangeDutyCycle(0)
    p.ChangeFrequency(speed + 5)
    a.ChangeFrequency(speed + 5)
    
# reverse(speed): Sets both motors to reverse at speed. 0 <= speed <= 100
def reverse(speed):
    p.ChangeDutyCycle(0)
    q.ChangeDutyCycle(speed)
    a.ChangeDutyCycle(0)
    b.ChangeDutyCycle(speed)
    q.ChangeFrequency(speed + 5)
    b.ChangeFrequency(speed + 5)

# spinLeft(speed): Sets motors to turn opposite directions at speed. 0 <= speed <= 100
def spinRight(speed):
    p.ChangeDutyCycle(0)
    q.ChangeDutyCycle(speed)
    a.ChangeDutyCycle(speed)
    b.ChangeDutyCycle(0)
    q.ChangeFrequency(speed + 5)
    a.ChangeFrequency(speed + 5)
    
# spinRight(speed): Sets motors to turn opposite directions at speed. 0 <= speed <= 100
def spinLeft(speed):
    p.ChangeDutyCycle(speed)
    q.ChangeDutyCycle(0)
    a.ChangeDutyCycle(0)
    b.ChangeDutyCycle(speed)
    p.ChangeFrequency(speed + 5)
    b.ChangeFrequency(speed + 5)
    
# turnForward(leftSpeed, rightSpeed): Moves forwards in an arc by setting different speeds. 0 <= leftSpeed,rightSpeed <= 100
def turnForward(leftSpeed, rightSpeed):
    p.ChangeDutyCycle(leftSpeed)
    q.ChangeDutyCycle(0)
    a.ChangeDutyCycle(rightSpeed)
    b.ChangeDutyCycle(0)
    p.ChangeFrequency(leftSpeed + 5)
    a.ChangeFrequency(rightSpeed + 5)
    
# turnReverse(leftSpeed, rightSpeed): Moves backwards in an arc by setting different speeds. 0 <= leftSpeed,rightSpeed <= 100
def turnReverse(leftSpeed, rightSpeed):
    p.ChangeDutyCycle(0)
    q.ChangeDutyCycle(leftSpeed)
    a.ChangeDutyCycle(0)
    b.ChangeDutyCycle(rightSpeed)
    q.ChangeFrequency(leftSpeed + 5)
    b.ChangeFrequency(rightSpeed + 5)

# go(leftSpeed, rightSpeed): controls motors in both directions independently using different positive/negative speeds. -100<= leftSpeed,rightSpeed <= 100
def go(leftSpeed, rightSpeed):
    if leftSpeed<0:
        p.ChangeDutyCycle(0)
        q.ChangeDutyCycle(abs(leftSpeed))
        q.ChangeFrequency(abs(leftSpeed) + 5)
    else:
        q.ChangeDutyCycle(0)
        p.ChangeDutyCycle(leftSpeed)
        p.ChangeFrequency(leftSpeed + 5)
    if rightSpeed<0:
        a.ChangeDutyCycle(0)
        b.ChangeDutyCycle(abs(rightSpeed))
        p.ChangeFrequency(abs(rightSpeed) + 5)
    else:
        b.ChangeDutyCycle(0)
        a.ChangeDutyCycle(rightSpeed)
        p.ChangeFrequency(rightSpeed + 5)

# go(speed): controls motors in both directions together with positive/negative speed parameter. -100<= speed <= 100
def goBoth(speed):
    if speed<0:
        reverse(abs(speed))
    else:
        forward(speed)

# End of Motor Functions
#======================================================================        
screen = curses.initscr()
curses.noecho()
curses.cbreak()
screen.keypad(True)
X = 10
init()
try:
    while True:
        char=screen.getch()
        if char==ord('q'):
            break
        elif char==curses.KEY_RIGHT:
            spinRight(X)
        elif char==curses.KEY_LEFT:
            spinLeft(X)
        elif char==curses.KEY_DOWN:
            reverse(X)
        elif char==curses.KEY_UP:
            forward(X)
        elif char==ord('b'):
            stop()
        elif char==ord('z'):
            X+=10
            if X>100:
                X=100
        elif char==ord('x'):
            X-=10
            if X<0:
                X=0

finally:
    curses.nocbreak()
    screen.keypad(0)
    curses.echo()
    curses.endwin()
    cleanup()
    print ('HELLO')
    sys.exit(1)

