#!/usr/bin/env python

from __future__ import division
import math

# z is up
# x is sideways
# y is depth

#================================================================================

def binarySearch(fn, xmin, xmax, desiredY, epsilon = 0.001):
    """Given a function, find the x where it has the desired value desiredY = fn(x).
    Search between xmin and xmax.
    The function must be monotonic.
    If the function does not cross desiredY, throw an assertion error.
    """
    if abs(xmin - xmax) < epsilon:
        return (xmin + xmax) / 2
    f0 = fn(xmin)
    f1 = fn(xmax)
    assert (f0 < desiredY) != (f1 < desiredY)
    xmid = (xmin + xmax)/2
    fmid = fn(xmid)
    if (f0 < desiredY) == (fmid < desiredY):
        return binarySearch(fn, xmid, xmax, desiredY, epsilon)
    elif (f1 < desiredY) == (fmid < desiredY):
        return binarySearch(fn, xmin, xmid, desiredY, epsilon)

def makeCircleSegment(rad, striplen, numLeds, degreeOffset=0):
    """Make a circle segment which wraps as far around the circle as striplen will reach.
    Start at the right side of the circle, going upward
    """
    result = []
    maxtheta = striplen / rad
    for ii in range(numLeds):
        pct = ii/numLeds
        theta = maxtheta * pct
        theta += degreeOffset * math.pi / 180
        x = rad * math.cos(theta)
        z = rad * math.sin(theta)
        result.append((x, 0, z))
    return result

def transform(points, amount):
    ax, ay, az = amount
    return [(px+ax, py+ay, pz+az) for px, py, pz in points]

def scale(points, amount):
    ax, ay, az = amount
    return [(px*ax, py*ay, pz*az) for px, py, pz in points]

def row(start, direction, count):
    # assume direction is normalized
    sx, sy, sz = start
    dx, dy, dz = direction
    result = []
    for ii in range(count):
        result.append(( sx + dx * ii * METERS_PER_LED,
                        sy + dy * ii * METERS_PER_LED,
                        sz + dz * ii * METERS_PER_LED ))
    return result

#================================================================================

FT_TO_M = 0.3048

HALF_TABLE_WIDTH = 4 * FT_TO_M
SHADE_CELL_WIDTH = 10 * FT_TO_M
SHADE_CELL_HEIGHT = 8 * FT_TO_M
SHADE_DEPTH = 7 * FT_TO_M
CIRCLE_HEIGHT = 1.7  # tabletop to center of circle
STRIP_LEN = 5
LEDS_PER_METER = 32
LEDS_PER_FOOT = int(LEDS_PER_METER * FT_TO_M) # rounded
LEDS_PER_STRIP = 160
METERS_PER_LED = 1 / LEDS_PER_METER
CORNER_OFFSET_LEDS = 1 * LEDS_PER_FOOT # how many leds to shift the strips around the corners
TABLE_HEIGHT = 3 * FT_TO_M

def computeXgivenR(r):
    theta = STRIP_LEN / r
    x = r - r * math.cos(theta)
    return x

CURVE_RADIUS = binarySearch(computeXgivenR, 2.3, 50, HALF_TABLE_WIDTH)
CURVE_THETA = STRIP_LEN / CURVE_RADIUS

# origin is center front bottom of arch, on the tabletop

leftCurvePoints = transform(    makeCircleSegment(CURVE_RADIUS, STRIP_LEN, LEDS_PER_STRIP),
                                (-CURVE_RADIUS+HALF_TABLE_WIDTH,0,0)    )
rightCurvePoints = scale(leftCurvePoints, (-1,1,1))

circlePoints = transform(   makeCircleSegment(STRIP_LEN / (2*math.pi), STRIP_LEN, LEDS_PER_STRIP, -90),
                            (0,0,CIRCLE_HEIGHT)    )

# make shade parts.  origin is center front bottom of table, on the ground
rightColumn = row( (-1.5 * SHADE_CELL_WIDTH, -SHADE_DEPTH, SHADE_CELL_HEIGHT), (0,0,-1), LEDS_PER_STRIP / 2 - CORNER_OFFSET_LEDS)
rightRow = row( (-1.5 * SHADE_CELL_WIDTH, -SHADE_DEPTH, SHADE_CELL_HEIGHT), (1,0,0), LEDS_PER_STRIP / 2 + CORNER_OFFSET_LEDS)

# move shade parts down by TABLE_HEIGHT so origin is on the tabletop to match the arch's origin
rightColumn = transform(rightColumn, (0,0,-TABLE_HEIGHT))
rightRow = transform(rightRow, (0,0,-TABLE_HEIGHT))

leftColumn = scale(rightColumn, (-1,1,1))
leftRow = scale(rightRow, (-1,1,1))

points = []
points += circlePoints
points += leftCurvePoints
points += reversed(rightCurvePoints)
points += reversed(rightColumn)
points += rightRow
points += reversed(leftRow)
points += leftColumn

# # helper marker dots
# points.append((-1.5 * SHADE_CELL_WIDTH, -SHADE_DEPTH, -TABLE_HEIGHT))
# points.append((1.5 * SHADE_CELL_WIDTH, -SHADE_DEPTH, -TABLE_HEIGHT))
# points.append((-0.5 * SHADE_CELL_WIDTH, -SHADE_DEPTH, -TABLE_HEIGHT))
# points.append((0.5 * SHADE_CELL_WIDTH, -SHADE_DEPTH, -TABLE_HEIGHT))
# points.append((-0.5 * SHADE_CELL_WIDTH, -SHADE_DEPTH, -TABLE_HEIGHT+SHADE_CELL_HEIGHT))
# points.append((0.5 * SHADE_CELL_WIDTH, -SHADE_DEPTH, -TABLE_HEIGHT+SHADE_CELL_HEIGHT))
# points.append((HALF_TABLE_WIDTH, 0, -TABLE_HEIGHT))
# points.append((-HALF_TABLE_WIDTH, 0, -TABLE_HEIGHT))

# transform so the circle is at the origin
points = transform(points, (0,0,-CIRCLE_HEIGHT))

# convert to JSON and print
result = ['[']
for point in points:
    result.append('  {"point": [%.4f, %.4f, %.4f]},' % point)
result[-1] = result[-1][:-1]  # trim off last comma
result.append(']')
print '\n'.join(result)






















