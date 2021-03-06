#!/usr/bin/env python3

MAP_SIZE_PIXELS         = 500
MAP_SIZE_METERS         = 10
LIDAR_DEVICE            = 'COM9'

# Ideally we could use all 250 or so samples that the RPLidar delivers in one 
# scan, but on slower computers you'll get an empty map and unchanging position
# at that rate.
MIN_SAMPLES = 180

from breezyslam.algorithms import RMHC_SLAM
from breezyslam.sensors import RPLidarA1 as LaserModel

from rplidar import RPLidar as Lidar

from roboviz import MapVisualizer

from scipy.interpolate import interp1d
import numpy as np
from PIL import Image
import door as dr
import multiprocessing as mp

def saveimg(mapbytes,size):
    mapimg = np.reshape(np.frombuffer(mapbytes, dtype=np.uint8), (size, size))
    img,img_arr = dr.detect_doors(mapimg)
    img.save('my.png')

    
if __name__ == '__main__':

    # Connect to Lidar unit
    lidar = Lidar(LIDAR_DEVICE)

    # Create an RMHC SLAM object with a laser model and optional robot model
    slam = RMHC_SLAM(LaserModel(), MAP_SIZE_PIXELS, MAP_SIZE_METERS)

    # Set up a SLAM display
    viz = MapVisualizer(MAP_SIZE_PIXELS, MAP_SIZE_METERS, 'SLAM')

    # Initialize an empty trajectory
    trajectory = []

    # Initialize empty map
    mapbytes = bytearray(MAP_SIZE_PIXELS * MAP_SIZE_PIXELS)

    # Create an iterator to collect scan data from the RPLidar
    iterator = lidar.iter_scans(max_buf_meas=500)

    # We will use this to store previous scan in case current scan is inadequate
    previous_distances = None

    # First scan is crap, so ignore it
    next(iterator)
    mp.set_start_method('spawn')
    q = mp.Queue()
    p = mp.Process(target=dr.detect_doors, args=(q,))
    p.start()
    while True:

        # Extrat (quality, angle, distance) triples from current scan
        items = [item for item in next(iterator)]

        # Extract distances and angles from triples
        distances = [item[2] for item in items]
        angles    = [item[1] for item in items]

        print(len(distances))

        # Update SLAM with current Lidar scan and scan angles if adequate
        if len(distances) > MIN_SAMPLES:

            # First interpolate to get 360 angles from 0 through 359, and corresponding distances
            f = interp1d(angles, distances, fill_value='extrapolate')
            distances = list(f(np.arange(360))) # slam.update wants a list

            # Then update with interpolated distances
            slam.update(distances)

            # Store interplated distances for next time
            previous_distances = distances.copy()

        # If not adequate, use previous
        elif previous_distances is not None:
            slam.update(previous_distances)

        # Get current robot position
        x, y, theta = slam.getpos()

        # Get current map bytes as grayscale
        slam.getmap(mapbytes)
        # Display map and robot pose, exiting gracefully if user closes it
        if not viz.display(x/1000., y/1000., theta, mapbytes):
            #saveimg(mapbytes,MAP_SIZE_PIXELS)
            lidar.stop()
            lidar.disconnect()
            q.put("quit")
            exit(0)
        else:
            mapimg = np.reshape(np.frombuffer(mapbytes, dtype=np.uint8), (500, 500))
            q.put(mapimg)
 
    # Shut down the lidar connection
    lidar.stop()
    lidar.disconnect()