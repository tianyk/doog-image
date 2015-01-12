#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random
from PIL import Image, ImageDraw, ImageColor

for i in range(1, 11):
    im = Image.new('RGB', (300, 500), '#6699CC')
    draw = ImageDraw.Draw(im)
    draw.text((148, 30), str(i))
    im.save(str(i) + '.jpg')
