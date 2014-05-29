# -*- coding: utf-8 -*-
__author__ = 'Impressed'

class mydict(dict):
    def __getattr__(self, key):
        try:
            return self.key
        except:
            return self[key]
    def __setattr__(self, key, value):
        self[key] = value

# try it
newdict = mydict(first = 'element', second = 'pocemon')

print (newdict.first)


