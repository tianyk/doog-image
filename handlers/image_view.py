#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import division

import re
import logging
import tornado.web
from PIL import Image

from base_image import BaseImageHandler

IMAGE_INFO = "imageInfo"
IMAGE_VIEW = "imageView"
EXIF       = "exif"
IMAGE_MOGR = "imageMogr"
WATER_MARK = "watermark"
IMAGE_AVE  = "imageAve"

class ImageViewHandler(BaseImageHandler):
    def get(self, file_name, ext):
        interface = self.get_argument("interface", None)

        file_path = 'upload' + self.request.path
        try:
            im = Image.open(file_path)
        except IOError:
            write_blank()

        if not interface: # 直接返回原图
            self.write_image(im, file_name, ext)

        elif IMAGE_INFO == interface: # 图片基本信息
            size = im.size
            info               = {}
            info["format"]     = im.format or 'None'
            info["width"]      = size[0]
            info["height"]     = size[1]
            info["colorModel"] = im.mode

            self.write(info)
        elif IMAGE_VIEW == interface: # 图片处理
            interface = self.get_argument("interface", None)
            mode      = self.get_argument("mode", None)
            w         = self.get_argument("w", None)
            h         = self.get_argument("h", None)

            size = im.size
            if "0"   == mode:
                if w and int(w) > size[0]:
                    w = size[0]
                if h and int(h) > size[1]:
                    h = size[1]

                if w and h:
                    pass
                elif w:
                    w = int(w)
                    h = int(size[1] * (w / size[0]))
                elif h:
                    h = int(h)
                    w = int(size[0] * (h / size[1]))
                else:
                    pass

                im = im.resize((w, h))
                self.write_image(im, file_name, ext)
            elif "1" == mode:
                if not w and not h: # 暂时返回原图，后期改为参数错误
                    self.write_image(im, file_name, ext)
                    return

                if not w:
                    w = h
                if not h:
                    h = w
                w = int(w)
                h = int(h)

                ratio_w = ratio_h = 1
                if w:
                    ratio_w = w / size[0]
                if h:
                    ratio_h = h / size[1]
                ratio = max(ratio_w, ratio_h, 1)

                resize = []
                box = [0, size[0], size[1], 0]
                if 1 != ratio: # > 1 resize
                    if ratio_w > ratio_h:
                        resize = tuple(int(x * ratio_w) for x in size)
                        box[0] = 0
                        box[2] = w
                        box[1] = int(h * (ratio_w - 1) / 2)
                        box[3] = h + box[1]
                    else:
                        resize = tuple(int(x * ratio_h) for x in size)
                        box[1] = 0
                        box[3] = h
                        box[0] = int(w * (ratio_h - 1) / 2)
                        box[2] = w + box[0]

                    resize = tuple(resize)
                    im = im.resize(resize)
                else: # ratio <= 1 no resize
                    box[0] = int((size[0] - w) / 2)
                    box[2] = w + box[0]
                    box[1] = int((size[1] - h) / 2)
                    box[3] = h + box[1]

                im = im.crop(tuple(box))
                self.write_image(im, file_name, ext)

            elif "2" == mode:
                pass
            elif "3" == mode:
                pass
            elif "4" == mode:
                pass
            elif "5" == mode:
                pass
            else:
                self.write_image(im, file_name, ext)
        elif EXIF       == interface:
            pass
        elif IMAGE_MOGR == interface:
            pass
        elif WATER_MARK == interface:
            pass
        elif IMAGE_AVE  == interface:
            pass
        else: # 直接返回原图
            self.write_image(im, file_name, ext)