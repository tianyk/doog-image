#!/usr/bin/env python# -*- coding: utf-8 -*-__author__ = 'tyk'from PIL import Image, ExifTagsfile_path = "E:/17629705.jpg"im = Image.open(file_path)exif = im._getexif()if exif:    orientation = exif.get(0x0112, None)    print(orientation)# im.show()# im.rotate(90).show()# im.rotate(180).show()# im.rotate(270).show()# im.rotate(360).show()# im.rotate(0).show()# im.transpose(Image.ROTATE_180).show()im.show()# im.transpose(Image.FLIP_LEFT_RIGHT).show() # 左右翻转# im.transpose(Image.FLIP_TOP_BOTTOM).show() # 上下翻转im.transpose(Image.TRANSPOSE).show() # 逆时针90度，加上下翻转im.transpose(Image.ROTATE_90).transpose(Image.FLIP_TOP_BOTTOM).show()# im.transpose(Image.ROTATE_90).show() # 逆时针90度# ROTATE_90 = 2# ROTATE_180 = 3# ROTATE_270 = 4# TRANSPOSE = 5