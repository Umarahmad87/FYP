import curses
import RPi.GPIO as gpio

yellow = 29
red = 35
orange= 37
brown = 31

gpio.setmode(gpio.BOARD)
gpio.setup(yellow,gpio.OUT)
gpio.setup(brown,gpio.OUT)
gpio.setup(red,gpio.OUT)
gpio.setup(orange,gpio.OUT)

screen = curses.initscr()
curses.noecho()
curses.cbreak()
screen.keypad(True)

try:
    while True:
        char=screen.getch()
        if char==ord('q'):
            break
        elif char==curses.KEY_UP:
            gpio.output(yellow,False)
            gpio.output(brown,False)
            gpio.output(red,True)
            gpio.output(orange,True)
        elif char==curses.KEY_DOWN:
            gpio.output(yellow,True)
            gpio.output(brown,True)
            gpio.output(red,False)
            gpio.output(orange,False)
        elif char==curses.KEY_LEFT:
            gpio.output(yellow,False)
            gpio.output(brown,True)
            gpio.output(red,False)
            gpio.output(orange,True)
        elif char==curses.KEY_RIGHT:
            gpio.output(yellow,True)
            gpio.output(brown,False)
            gpio.output(red,True)
            gpio.output(orange,False)
        elif char==ord('z'):
            gpio.output(yellow,False)
            gpio.output(brown,False)
            gpio.output(red,False)
            gpio.output(orange,False)

finally:
    curses.nocbreak()
    screen.keypad(0)
    curses.echo()
    curses.endwin()
    gpio.cleanup()
    print ('HELLO')
    