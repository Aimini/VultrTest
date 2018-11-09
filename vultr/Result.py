# -*- coding: utf-8 -*-
# time: 2018-11-06 19:46:13
# Author: AI

class Result:
    def __init__(self, cs=None, sc=None, speed=None):
        if speed is None:
            speed = {}
        if cs is None:
            cs = {}
        if sc is None:
            sc = {}
        self.cs = cs
        self.sc = sc
        self.speed = speed

    def as_list(self):
        l = []
        l.extend([i for i in self.cs["package"]])
        l.extend([i for i in self.cs["delay"]])
        l.extend([i for i in self.sc["package"]])
        l.extend(self.sc["delay"])
        l.extend(self.speed)
        return l

    def __repr__(self):
        return str(vars(self))
