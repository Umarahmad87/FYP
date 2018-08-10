from Robot_Canvas import *
import numpy as np

R = Canvas()
while True:
    deg=int(input('Enter degree:'))
    dist=int(input('Enter distance:'))
    R.update_position(deg,dist,True)