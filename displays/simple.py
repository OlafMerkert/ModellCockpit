#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import division

__author__ = "Olaf Merkert"

from errorrep import UnimplementedMethod
from PyQt4 import QtCore, QtGui
import numpy as np

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

class Display (object):

    def __init__(self, name, interval, unit):
         self._name = name
         # TODO Verarbeiten der Bereichsgrenzen
         # TODO Unterstuetzung fuer dynamische Skalierung
         self._interval = interval
         self._unit = unit

    def get_lower(self):
        return self._interval[0]

    def get_upper(self):
        return self._interval[1]

    def put(self, data):
        self._value = data
        self._put(data)

    def _put(self, data):
        raise UnimplementedMethod()

class CircularDisplay (QtGui.QWidget, Display):

    def __init__(self, name, interval, unit):
        QtGui.QWidget.__init__(self)
        Display.__init__(self, name, interval, unit)
        self._value = 0
        self.setupUi()

    def _put(self, data):
        # TODO Benachrichtigung zum Neuzeichnen
        pass
    
    def setupUi(self):
        self.setGeometry(0, 0, 300, 300)
        self.setWindowTitle("Circular Display")

    def paintEvent(self, event):
        painter = QtGui.QPainter()
        painter.begin(self)
        self.drawDisk(painter)
        self.drawTicks(painter)
        self.drawUnit(painter)
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

    def drawUnit(self, pa):
        la = select_color("labels")
        pa.setPen(la)
        pa.setFont(select_font(20))
        pa.drawText(100, 240, 100, 40,
                    QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter,
                    "[%s]" % self._unit)

    def drawIndicator(self, pa):
        # Rechne den Winkel
        l, u = self.get_lower(), self.get_upper()
        la, ua = 0.1 *2*np.pi, 0.9 *2*np.pi
        angle = (self._value - l) / (u - l) * (ua - la) + la
        all_angles = np.array([angle - np.pi/2, angle, angle + np.pi/2, angle + np.pi])
        # Rechne die Position
        scales = np.array([15, 100, 15, 30])
        size = 150 
        x_pos, y_pos = (size + scales * (- np.sin(all_angles)),
                        size - scales * (- np.cos(all_angles)))
        # Fuellfarbe
        ind = select_color("indicator")
        pa.setBrush(ind)
        # Zeichne den Zeiger
        indicator = QtGui.QPolygonF([QtCore.QPointF(x,y) for x,y in zip(x_pos, y_pos)])
        pa.drawPolygon(indicator)

            
# TODO aktiviere Antialiasing fuer Kreise und Strecken

def bsp():
    d = CircularDisplay("Drehzahl", [0,1000], "rpm")
    d.show()
    return d
