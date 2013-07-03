#!/usr/bin/env python

"""A demo client for Open Pixel Control
http://github.com/zestyping/openpixelcontrol

Creates moving blobby colors.

To run:
First start the gl simulator using, for example, the included "wall" layout

    make
    bin/gl_server layouts/wall.json

Then run this script in another shell to send colors to the simulator

    example_clients/lava_lamp.py --layout layouts/wall.json

"""

from __future__ import division
import time
import sys
import optparse
import random
try:
    import json
except ImportError:
    import simplejson as json

import opc
import color_utils


#-------------------------------------------------------------------------------
# command line

parser = optparse.OptionParser()
parser.add_option('-l', '--layout', dest='layout',
                    action='store', type='string',
                    help='layout file')
parser.add_option('-s', '--server', dest='server', default='127.0.0.1:7890',
                    action='store', type='string',
                    help='ip and port of server')
parser.add_option('-f', '--fps', dest='fps', default=20,
                    action='store', type='int',
                    help='frames per second')

options, args = parser.parse_args()

if not options.layout:
    parser.print_help()
    print
    print 'ERROR: you must specify a layout file using --layout'
    print
    sys.exit(1)


#-------------------------------------------------------------------------------
# parse layout file

print
print '    parsing layout file'
print

coordinates = []
for item in json.load(open(options.layout)):
    if 'point' in item:
        coordinates.append(tuple(item['point']))

min_coord = (min(c[0] for c in coordinates), min(c[1] for c in coordinates), min(c[2] for c in coordinates))
max_coord = (max(c[0] for c in coordinates), max(c[1] for c in coordinates), max(c[2] for c in coordinates))


#-------------------------------------------------------------------------------
# connect to server

client = opc.Client(options.server)
if client.can_connect():
    print '    connected to %s' % options.server
else:
    # can't connect, but keep running in case the server appears later
    print '    WARNING: could not connect to %s' % options.server
print


#-------------------------------------------------------------------------------
# color function

def pixel_color(t, coord, ii, n_pixels, random_values, min_coord, max_coord):
    """Compute the color of a given pixel.

    t: time in seconds since the program started.
    ii: which pixel this is, starting at 0
    coord: the (x, y, z) position of the pixel as a tuple
    n_pixels: the total number of pixels
    random_values: a list containing a constant random value for each pixel

    Returns an (r, g, b) tuple in the range 0-255

    """

    # slow down time a bit
    t *= 0.83

    # make moving stripes for x, y, and z
    x, y, z = coord

    # remap the bounding box of the layout to the range 0-1
#     xp = color_utils.remap(x, min_coord[0], max_coord[0], 0, 1)
#     yp = color_utils.remap(y, min_coord[1], max_coord[1], 0, 1)
#     zp = color_utils.remap(z, min_coord[2], max_coord[2], 0, 1)
# 
#     general_scale = (max_coord[0]-min_coord[0] + max_coord[1]-min_coord[1] + max_coord[2]-min_coord[2]) / 3
    z_scale = max_coord[2] - min_coord[2]
    side_scale = 1.7 # smaller numbers compress things horizontally
    xp = x / z_scale / side_scale
    yp = y / z_scale / side_scale
    zp = (z-min_coord[2]) / z_scale

    # bend space so that things seem to accelerate upwards
    zp = (zp + 0.05) ** 0.7

    # apply various wiggles to coordinate space
    zp1 = (  zp + color_utils.cos(xp, offset= t*0.33 + 8.63, period=0.15 * 1.7, minn=0, maxx=1) * 0.2
                + color_utils.cos(xp, offset=-t*0.23 + 2.43, period=0.34 * 1.7, minn=0, maxx=1) * 0.3  )

    zp2 = (  zp + color_utils.cos(xp, offset=-t*0.38 + 1.23, period=0.23 * 1.7, minn=0, maxx=1) * 0.2
                + color_utils.cos(xp, offset= t*0.23 + 2.53, period=0.63 * 1.7, minn=0, maxx=1) * 0.3  )
    zp3 = (  zp + color_utils.cos(xp, offset=-t*0.42 + 5.62, period=0.27 * 1.7, minn=0, maxx=1) * 0.2
                + color_utils.cos(xp, offset= t*0.20 + 3.07, period=0.55 * 1.7, minn=0, maxx=1) * 0.3  )
    zp4 = (  zp + color_utils.cos(xp, offset= t*0.36 + 4.81, period=0.20 * 1.7, minn=0, maxx=1) * 0.2
                + color_utils.cos(xp, offset=-t*0.26 + 7.94, period=0.67 * 1.7, minn=0, maxx=1) * 0.3  )

    # make basic vertical gradient
    vgrad = color_utils.cos(color_utils.clamp(zp, 0, 1), offset=0, period=2, minn=0, maxx=1)
#     vgrad = 1 - color_utils.clamp(zp, 0, 1)

    # smallest fastest noise
    noise_lit = (   color_utils.cos(xp,  offset=-4.37 * t/4, period=0.21)
                  + color_utils.cos(yp,  offset= 4.37 * t/4, period=0.21)
                  + color_utils.cos(zp1, offset= 4.37 * t,   period=0.21)  ) / 3

    # small fast noise
    noise_med = (   color_utils.cos(xp,  offset=-3 * t/4, period=0.3)
                  + color_utils.cos(yp,  offset= 3 * t/4, period=0.3)
                  + color_utils.cos(zp3, offset= 3 * t,   period=0.3)  ) / 3

    # big slow noise
    noise_big = (   color_utils.cos(xp,  offset=-0.9 * t/2, period=0.8)
                  + color_utils.cos(yp,  offset= 0.9 * t/2, period=0.8)
                  + color_utils.cos(zp4, offset= 0.9 * t,   period=0.8)  ) / 3

    # combine vgradient with noise
    v = (   vgrad 
          + color_utils.remap(noise_lit, 0,1, -1,1)*0.17
          + color_utils.remap(noise_med, 0,1, -1,1)*0.2
          + color_utils.remap(noise_big, 0,1, -1,1)*0.8
         )

    # apply sine contrast curve
#     v = color_utils.cos( color_utils.clamp(v,0,1), offset=0, period=2, minn=1, maxx=0 )

    # color map
    r = v ** 1 * 1.5
    g = v ** 1 * 0.65
    b = v ** 1 * 0.34

    r,g,b = color_utils.contrast((r,g,b), 0.7, 1.2)

#     r,g,b = color_utils.clip_black_by_luminance((r,g,b), 0.2)

    return (r*256, g*256, b*256)


#-------------------------------------------------------------------------------
# send pixels

print '    sending pixels forever (control-c to exit)...'
print

n_pixels = len(coordinates)
random_values = [random.random() for ii in range(n_pixels)]
start_time = time.time()
while True:
    t = time.time() - start_time
    pixels = [pixel_color(t*0.6, coord, ii, n_pixels, random_values, min_coord, max_coord) for ii, coord in enumerate(coordinates)]
    client.put_pixels(pixels, channel=0)
    time.sleep(1 / options.fps)

