#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import division

__author__ = "Olaf Merkert"

from errorrep import UnimplementedMethod
from PyQt4 import QtCore, QtGui
from math import log, ceil, floor


class MeterStack (QtGui.QWidget):

    types = {}

    def __init__(self, parent = None):
        QtGui.QWidget.__init__(self, parent = parent)
        self.layout = QtGui.QHBoxLayout()
        self.setLayout(self.layout)
        self.meters = []

    def create_display(self, name, type, interval="dynamic", unit=""):
        c = self.types[type]

        m = c(name=name, interval=interval, unit=unit)
        self.meters.append(m)
        self.layout.addWidget(m)
        return m

    @classmethod
    def register(cls, type, clss):
        cls.types[type] = clss
        return clss

    def show(self):
        QtGui.QWidget.show(self)


def downscale(x):
    """Erniedrige x bis zur naechsten Groessenordnung"""
    if x == 0:
        return 0
    y = 10 ** floor( log(abs(x), 10) )
    return y * floor(x/y)

def upscale(x):
    """Erhoehe x bis zur naechsten Groessenordnung"""
    if x == 0:
        return 0
    y = 10 ** floor( log(abs(x), 10) )
    return y * ceil(x/y)


class Display (object):

    def __init__(self, name, interval, unit):
         self._name = name
         # Verarbeiten der Bereichsgrenzen
         # Unterstuetzung fuer dynamische Skalierung
         if interval == "dynamic":
             self._dynamic = True
             self._lower, self._upper = 0, 0
         else:
             self._dynamic = False
             self._lower, self._upper = interval
         self._unit = unit

    def get_lower(self):
        return self._lower

    def get_upper(self):
        return self._upper

    def put(self, data):
        self._value = data
        if self._dynamic and not \
               (self._lower <= data <= self._upper):
            self.recalc_bounds(data)

    def recalc_bounds(self, data):
        if self._lower > data:
            self._lower = downscale(data)
        if data > self._upper:
            self._upper = upscale(data)

