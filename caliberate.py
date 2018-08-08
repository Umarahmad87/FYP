import pandas as pd
import time
from comp import Compass
C = Compass()
"""
Data = pd.DataFrame()
values = []
xvalues = []
yvalues = []
minx = 0
maxx = 0
miny = 0
maxy = 0
for i in xrange(1000):
    x,y,val = C.getReadings()
    values.append(val)
    xvalues.append(x)
    yvalues.append(y)
    print "heading: %d"%val
    if x < minx:
        minx=x

    if y < miny:
        miny=y

    if x > maxx:
        maxx=x

    if y > maxy:
        maxy=y
    time.sleep(0.1)

Data['X'] = xvalues
Data['Y'] = yvalues
Data['heading'] = values
print "minx: ", minx
print "miny: ", miny
print "maxx: ", maxx
print "maxy: ", maxy
print "x offset: ", (maxx + minx) / 2
print "y offset: ", (maxy + miny) / 2

Data.to_csv('compassValues.csv',index=False)

"""
while True:
    print"heading: %d"%C.getAngle()
