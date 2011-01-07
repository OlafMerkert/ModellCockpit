#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import division

__author__ = "Olaf Merkert"

from errorrep import UnimplementedMethod
from PyQt4 import QtCore, QtGui
import numpy as np
from math import log, ceil, floor

colortheme = {
    "background": "b1b1b6ff",
    "foreground": "666b72ff",
    "ridge":      "4d4d57ff",
    "labels":     "070d19ff",
    "ticks":      "e4e4e5ff",
    "indicator":  "ac2a1fff",
    }

fontname = "Sans Serif"

def select_color(part):
    html_code = "#" + colortheme[part][0:6]
    return QtGui.QColor(html_code)

def select_font(size):
    return QtGui.QFont(fontname, size)

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
         # TODO Verarbeiten der Bereichsgrenzen
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
        if self._dynamic:
            self.recalc_bounds(data)
        self._put(data)

    def recalc_bounds(self, data):
        if self._lower > data:
            self._lower = downscale(data)
        if data > self._upper:
            self._upper = upscale(data)

    def _put(self, data):
        raise UnimplementedMethod()

class CircularDisplay (QtGui.QWidget, Display):

    def __init__(self, name, interval, unit):
        QtGui.QWidget.__init__(self)
        Display.__init__(self, name, interval, unit)
        self._value = 0
        self.setupUi()

    def _put(self, data):
        # Benachrichtigung zum Neuzeichnen
        self.update()
    
    def setupUi(self):
        self.setGeometry(0, 0, 300, 300)
        self.setWindowTitle("Circular Display")

    def paintEvent(self, event):
        painter = QtGui.QPainter()
        painter.begin(self)
        # Aktiviere Antialiasing
        painter.setRenderHint(QtGui.QPainter.Antialiasing, True)
        painter.setRenderHint(QtGui.QPainter.TextAntialiasing, True)
        self.drawDisk(painter)
        self.drawTicks(painter)
        self.drawLabels(painter)
        self.drawIndicator(painter)
        self.drawNotch(painter)
        painter.end()

    def drawDisk(self, pa):
        bg = select_color("background")
        ri = select_color("ridge")
        pa.setBrush(bg)
        pen = QtGui.QPen(ri, 5, QtCore.Qt.SolidLine)
        pa.setPen(pen)
        # TODO anpassen fuer nicht-fixe Groesse
        shrink = 5
        pa.drawEllipse(shrink, shrink, # Ecke
                       300 - 2*shrink, 300 - 2*shrink) # Breite, Hoehe

    def drawNotch(self, pa):
        fg = select_color("foreground")
        ri = select_color("ridge")
        pa.setBrush(fg)
        pen = QtGui.QPen(ri, 3, QtCore.Qt.SolidLine)
        pa.setPen(pen)
        # TODO anpassen fuer nicht-fixe Groesse
        radius = 20
        shrink = 150 - radius
        pa.drawEllipse(shrink, shrink, # Ecke
                       300 - 2*shrink, 300 - 2*shrink) # Breite, Hoehe

    def drawTicks(self, pa):
        # Berechne die Positionen fuer die gewuenschte Anzahl von
        # Markierungen
        nr = 11
        angles = np.linspace(0.1 * 2*np.pi, 0.9 * 2*np.pi, nr)
        labels = np.linspace(self.get_lower(), self.get_upper(), nr)
        x_pos = - np.sin(angles)
        y_pos = - np.cos(angles)
        # Bestimme Positionen fuer Anfang/Ende der Striche und
        # Beschriftungen
        size = 150
        def scale_and_transform(x, y, scaling):
            return (size + scaling * size * x,
                    size - scaling * size * y)
        start_x, start_y = scale_and_transform(x_pos, y_pos, 0.8)
        end_x, end_y     = scale_and_transform(x_pos, y_pos, 0.9)
        label_x, label_y = scale_and_transform(x_pos, y_pos, 0.7)
                       
        # Zeichne die Striche
        ti = select_color("ticks")
        # pa.setBrush(None)
        pen = QtGui.QPen(ti, 7, QtCore.Qt.SolidLine)
        pa.setPen(pen)
        for coords in zip(start_x, start_y,
                                  end_x,   end_y):
            pa.drawLine(*coords)
        # Zeichne die Beschriftung der Striche
        pa.setPen(ti)
        pa.setFont(select_font(12))
        for x, y, label in zip(label_x, label_y, labels):
            # TODO Bessere Formatierung der Beschriftung
            # TODO Elegantere Ausrichtung des Texts
            pa.drawText(x - 40, y - 10, 80, 20,
                        QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter,
                        "%d" % label)

    def drawLabels(self, pa):
        la = select_color("labels")
        pa.setPen(la)
        pa.setFont(select_font(20))
        pa.drawText(100, 240, 100, 40,
                    QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter,
                    "[%s]" % self._unit)
        pa.setFont(select_font(16))
        pa.drawText(100, 180, 100, 30,
                    QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter,
                    self._name)

    def drawIndicator(self, pa):
        # Rechne den Winkel
        l, u = self.get_lower(), self.get_upper()
        la, ua = 0.1 *2*np.pi, 0.9 *2*np.pi
        try:
            s = (ua - la) / (u - l)
        except ZeroDivisionError:
            s = 1
        angle = (self._value - l) * s  + la
        all_angles = np.array([angle - np.pi/2, angle, angle + np.pi/2, angle + np.pi])
        # Rechne die Position
        scales = np.array([15, 100, 15, 30])
        size = 150 
        x_pos, y_pos = (size + scales * (- np.sin(all_angles)),
                        size - scales * (- np.cos(all_angles)))
        # Fuellfarbe
        ind = select_color("indicator")
        pa.setBrush(ind)
        pa.setOpacity(0.8)
        # Zeichne den Zeiger
        indicator = QtGui.QPolygonF([QtCore.QPointF(x,y) for x,y in zip(x_pos, y_pos)])
        pa.drawPolygon(indicator)
        pa.setOpacity(1)

