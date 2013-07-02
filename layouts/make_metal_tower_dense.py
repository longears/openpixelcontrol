#!/usr/bin/env python

from __future__ import division
import json

points = []

def column(base, height, density=32):
    result = []
    count = height * density
    for ii in range(count):
        x, y, z = base
        z += ii/density
        result.append((x,y,z))
    return result

points +=          column((-2, 0, 0.0-1), 2)
points += reversed(column((-1, 0, 0.5-1), 2))
points +=          column(( 0, 0, 1.0-1), 2)
points += reversed(column(( 1, 0, 0.5-1), 2))
points +=          column(( 2, 0, 0.0-1), 2)


result = ['[']
for point in points:
    result.append('  {"point": [%.4f, %.4f, %.4f]},' % point)

# trim off last comma
result[-1] = result[-1][:-1]

result.append(']')
print '\n'.join(result)



#
