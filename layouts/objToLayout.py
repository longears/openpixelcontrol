#!/usr/bin/env python

import sys

#--------------------------------------------------------------------------------
# UTLS

def readFile(fn):
    f = file(fn,'r'); data = f.read(); f.close(); return data

def writeFile(fn, data):
    f = file(fn,'w'); f.write(data); f.close()

#--------------------------------------------------------------------------------
# HELPERS

def getObjVerts(fn):
    """Return a list of (x,y,z) as strings
    """
    data = readFile(fn)
    verts = []
    for line in data.splitlines():
        if line.startswith('v '):
            v, x, y, z = line.split()
            verts.append((x, y, z))
    return verts

#--------------------------------------------------------------------------------
# MAIN

if __name__ == '__main__':
    ARGS = sys.argv[1:]
    if len(ARGS) != 1 or ARGS[0] in ('-h', '--help'):
        print 'usage: objToLayout.py  myfile.obj'
        sys.exit(0)
    objFn = ARGS[0]
    layoutFn = objFn.replace('.obj', '.json')

    print
    print 'reading %s' % objFn
    verts = getObjVerts(objFn)
    print '%s vertices found' % len(verts)

    layout = ["["]
    for x,y,z in verts:
        # swap y and z
        layout.append("""  {"point": [%s, %s, %s]},""" % (z, x, y))
    layout = '\n'.join(layout)
    layout = layout[:-1] # remove last comma
    layout += '\n]'
#     print layout

    print 'saving to %s' % layoutFn
    writeFile(layoutFn, layout)
    print








