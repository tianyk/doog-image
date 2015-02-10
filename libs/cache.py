#!/usr/bin/env python# -*- coding: utf-8 -*-__author__ = 'tyk'import base64import functoolsimport memcacheimport image_utilsmc = memcache.Client(['10.101.110.17:11211'])def load_image(func):    @functools.wraps(func)    def wrapper(*args, **kw):        that = args[0]        ext = args[2]        uri = that.uri        key = base64.urlsafe_b64encode(uri)        try:            image_data = mc.get(key)            format = mc.get("format_" + key) or ext            if image_data:                # TODO 在write_image上绑定的有cache_image，会多一次Cache.                # 此ext不一定是真实的格式，如果存在format.                that.write_image(image_data, format)                return        except:            pass        return func(*args, **kw)    return wrapperdef cache_image(func):    @functools.wraps(func)    def wrapper(*args, **kw):        that = args[0]        uri = that.uri        key = base64.urlsafe_b64encode(uri)        image_data = args[1]        format = args[2]        try:            mc.set("format_" + key, format)            mc.set(key, image_data)        except:            pass        return func(*args, **kw)    return wrapper# class Request:#     @load_image#     def get(self, image_name):#         print 'Get Image: ', image_name##     def write_image(self, im):#         print 'Write Image: ', im##     @cache_image#     def write_image_cached(self, *args):#         self.write_image(*args)### req = Request()# req.write_image_cached('007.jpg')# req.get('008.jpg')## memcache.Client