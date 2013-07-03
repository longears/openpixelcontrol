#!/usr/bin/env python

from __future__ import division
import sys
import math
import json

points = []
DENSITY = 12.5

SCALE = 0.5

def circle(center, normal="y", rad=1, density=DENSITY):
    result = []
    circum = rad * 2 * math.pi
    count = circum * density
    cx, cy, cz = center
    for ii in range(count):
        pct = ii/count
        a = math.cos(pct * 2 * math.pi) * rad
        b = math.sin(pct * 2 * math.pi) * rad
        if normal == 'x':
            result.append((cx, cy+a, cz+b))
        elif normal == 'y':
            result.append((cx+a, cy, cz+b))
        elif normal == 'z':
            result.append((cx+a, cy+b, cz))
    return result


def column(base, length, direction, density=DENSITY):
    dx, dy, dz = direction

    # normalize direction
    total = (dx**2 + dy**2 + dz**2) ** 0.5
    dx /= total
    dy /= total
    dz /= total

    result = []
    count = int(length * density + 0.5)
    for ii in range(count):
        x, y, z = base
        x += dx * ii/density
        y += dy * ii/density
        z += dz * ii/density
        result.append((x,y,z))
    return result

# circle
points += circle(  center=( 0.0, 0.0, 5.0), normal='y', rad=0.5  )

# vertical center
points += column(  base=( 1.5, 0.0, 0.0), length=6, direction=(0,0,1)  )
points += column(  base=(-1.5, 0.0, 0.0), length=6, direction=(0,0,1)  )

# vertical sides
points += column(  base=( 4.5, 0.0, 0.0), length=3, direction=(0,0,1)  )
points += column(  base=(-4.5, 0.0, 0.0), length=3, direction=(0,0,1)  )

# roof
points += column(  base=( 1.5, 0.0, 5.0), length=1.414 * 1.5, direction=(-1,0,1)  )
points += column(  base=(-1.5, 0.0, 5.0), length=1.414 * 1.5, direction=( 1,0,1)  )

# horizontal
points += column(  base=(-4.5, 0.0, 3.0), length=9, direction=(1,0,0)  )

# clothesline
points += column(  base=( 1.5, 0.0, 3.0), length=6, direction=(0,1,0)  )
points += column(  base=(-1.5, 0.0, 3.0), length=6, direction=(0,1,0)  )

# freestanding vertical parts
points += column(  base=( 1.5, 6.0, 0.0), length=3, direction=(0,0,1)  )
points += column(  base=(-1.5, 6.0, 0.0), length=3, direction=(0,0,1)  )


# apply scale
for ii in range(len(points)):
    points[ii] = (points[ii][0]*SCALE, points[ii][1]*SCALE, (points[ii][2]-3)*SCALE)

# convert to JSON and print
result = ['[']
for point in points:
    result.append('  {"point": [%.4f, %.4f, %.4f]},' % point)
result[-1] = result[-1][:-1]  # trim off last comma
result.append(']')
print '\n'.join(result)


sys.stderr.write('\n\n  %s LEDs, %s meters\n\n' % (len(points), len(points) / DENSITY))

#
