#!/usr/bin/env python

"""A demo client for Open Pixel Control
http://github.com/zestyping/openpixelcontrol

"""

from __future__ import division
import time
import math
import sys
import optparse

import opc
import color_utils


#-------------------------------------------------------------------------------
# command line

parser = optparse.OptionParser()
parser.add_option('-l', '--layout', dest='layout', default=None,
                    action='store', type='string',
                    help='layout file')
parser.add_option('-n', '--num', dest='num', default=0,
                    action='store', type='int',
                    help='number of leds')
parser.add_option('-s', '--server', dest='server', default='127.0.0.1:7890',
                    action='store', type='string',
                    help='ip and port of server')
parser.add_option('-f', '--fps', dest='fps', default=20,
                    action='store', type='int',
                    help='frames per second')

options, args = parser.parse_args()


#-------------------------------------------------------------------------------
# parse layout file

if options.layout:
    n_pixels = 0
    for item in json.load(open(options.layout)):
        if 'point' in item:
            n_pixels += 1
elif options.num:
    n_pixels = options.num
else:
    n_pixels = 100

print
print "    using %s pixels" % n_pixels
print


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
# send pixels

def main():
    print '    sending pixels forever (control-c to exit)...'
    print

    # how many sine wave cycles are squeezed into our n_pixels
    # 24 happens to create nice diagonal stripes on the wall layout
    freq_r = 24
    freq_g = 24
    freq_b = 24

    # how many seconds the color sine waves take to shift through a complete cycle
    speed_r = 7
    speed_g = -13
    speed_b = 19

    start_time = time.time()
    pixels = []
    for ii in range(n_pixels):
        pixels.append([0,0,0])

#     while True:
    for ii in xrange(1000):
        t = time.time() - start_time
        for ii in range(n_pixels):
            pct = ii / n_pixels
            r = pct * 256
            g = pct * 256
            b = pct * 256
    #         # diagonal black stripes
    #         pct_jittered = (pct * 77) % 37
    #         blackstripes = color_utils.cos(pct_jittered, offset=t*0.05, period=1, minn=-1.5, maxx=1.5)
    #         blackstripes_offset = color_utils.cos(t, offset=0.9, period=60, minn=-0.5, maxx=3)
    #         blackstripes = color_utils.clamp(blackstripes + blackstripes_offset, 0, 1)
    #         # 3 sine waves for r, g, b which are out of sync with each other
    #         r = blackstripes * color_utils.remap(math.cos((t/speed_r + pct*freq_r)*math.pi*2), -1, 1, 0, 256)
    #         g = blackstripes * color_utils.remap(math.cos((t/speed_g + pct*freq_g)*math.pi*2), -1, 1, 0, 256)
    #         b = blackstripes * color_utils.remap(math.cos((t/speed_b + pct*freq_b)*math.pi*2), -1, 1, 0, 256)
            pixel = pixels[ii]
            pixel[0] = r
            pixel[1] = g
            pixel[2] = b
        client.put_pixels(pixels, channel=0)

print '-------------- profiler off'
main()
print '-------------- profiler on'
import cProfile
cProfile.run('main()')

