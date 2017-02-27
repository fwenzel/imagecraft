#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time

from picraft import *
from PIL import Image


try:
    imagefile = sys.argv[1]
except IndexError:
    sys.exit('No filename specified!')

img = Image.open(imagefile)
pix = img.load()

if (img.mode in ('RGBA', 'LA') or
    img.mode == 'P' and 'transparency' in img.info):
    alpha = img.convert('RGBA').split()[-1]
else:
    alpha = None


world = World(host='10.11.12.133')

startpos = world.player.tile_pos + 3  # Roughly here.

ct = 0
for x in xrange(img.size[0]):
    for y in xrange(img.size[1]):

        # Don't render transparent pixels.
        if alpha and alpha.getpixel((x, y)) == 0:
            continue

        blockpos = startpos + Vector(x=x, y=img.size[1] - y)
        color = '#%02x%02x%02x' % pix[x, y][:3]
        world.blocks[blockpos] = Block(color)

        ct +=1
        if ct % 50 == 0:  # Give the server time to catch up every 50 blocks.
            print ct
            time.sleep(1)

print 'Done painting!'
