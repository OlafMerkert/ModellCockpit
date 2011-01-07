#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = "Olaf Merkert"

class MeterStack (object):
    types = {}

    def __init__(self):
        self.meters = []

    def show(self):
        pass

    def create_display(self, name, type, interval="dynamic", unit=""):
        c = self.types[type]

        m = c(name=name, interval=interval, unit=unit)
        self.meters.append(m)
        return m

    @classmethod
    def register(cls, type, clss):
        cls.types[type] = clss
        return clss

class PrintMeter (object):

    def __init__(self, name, interval, unit):
        self._name = name
        # TODO Intelligenteres Handling des Range
        self._interval = interval
        self._unit = unit

    def put(self, data):
        print "%s: %f [%s]" % (self._name, data, self._unit)

MeterStack.register("circular", PrintMeter)
MeterStack.register("light", PrintMeter)

