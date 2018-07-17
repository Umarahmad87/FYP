import curses
import RPi.GPIO as gpio
import time
import threading
from Queue import Queue
import sys

yellow = 29
red = 35
orange= 37
brown = 31
GPIO_TRIGGER = 12
GPIO_ECHO = 18
D_stop = Queue(maxsize=1)
ss = Queue(maxsize=1)
ss.put(True)
gpio.setmode(gpio.BOARD)
gpio.setup(GPIO_TRIGGER, gpio.OUT)
gpio.setup(GPIO_ECHO, gpio.IN)
gpio.setup(yellow,gpio.OUT)
gpio.setup(brown,gpio.OUT)
gpio.setup(red,gpio.OUT)
gpio.setup(orange,gpio.OUT)

screen = curses.initscr()
curses.noecho()
curses.cbreak()
screen.keypad(True)

def sonic_distance():
    while ss.get()==True:
    # set Trigger to HIGH
        gpio.output(GPIO_TRIGGER, True)
 
    # set Trigger after 0.01ms to LOW
        time.sleep(0.00001)
        gpio.output(GPIO_TRIGGER, False)
 
        StartTime = time.time()
        StopTime = time.time()
 
    # save StartTime
        while gpio.input(GPIO_ECHO) == 0:
            StartTime = time.time()
 
    # save time of arrival
        while gpio.input(GPIO_ECHO) == 1:
            StopTime = time.time()
 
    # time difference between start and arrival
        TimeElapsed = StopTime - StartTime
    # multiply with the sonic speed (34300 cm/s)
    # and divide by 2, because there and back
        distance = (TimeElapsed * 34300) / 2
        D_stop.put(distance)

def left(step=0.1):
    gpio.output(yellow,True)
    gpio.output(brown,True)
    gpio.output(red,False)
    gpio.output(orange,False)
    time.sleep(step)
    stop(0)
def right(step=0.1):
    gpio.output(yellow,False)
    gpio.output(brown,False)
    gpio.output(red,True)
    gpio.output(orange,True)
    time.sleep(step)
    stop(0)
def up(step=0.1):
    gpio.output(yellow,True)
    gpio.output(brown,False)
    gpio.output(red,True)
    gpio.output(orange,False)
    time.sleep(step)
    stop(0)
    right(0.13)
def down(step=0.1):
    gpio.output(yellow,False)
    gpio.output(brown,True)
    gpio.output(red,False)
    gpio.output(orange,True)
    time.sleep(step)
    stop(0)
    left()
def stop(step=0.1):
    gpio.output(yellow,False)
    gpio.output(brown,False)
    gpio.output(red,False)
    gpio.output(orange,False)
    time.sleep(step)
G = threading.Thread(target=sonic_distance)
G.start()
try:
    while True:
        try:
            d = D_stop.get()
            print d
            if d<=85:
                down(1)
        except:
            pass
        char=screen.getch()
        if char==ord('q'):
            break
        elif char==curses.KEY_RIGHT:
            right(0.3)
        elif char==curses.KEY_LEFT:
            left(0.3)
        elif char==curses.KEY_DOWN:
            down(1)
        elif char==curses.KEY_UP:
            up(1)
        elif char==ord('/'):
            stop()
        elif char==ord('a'):
            left()
        elif char==ord('d'):
            right()
        ss.put(True)

finally:
    curses.nocbreak()
    screen.keypad(0)
    curses.echo()
    curses.endwin()
    ss.put(False)
    gpio.cleanup()
    print ('HELLO')
    sys.exit(1)
    
