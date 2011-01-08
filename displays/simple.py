#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import division

__author__ = "Olaf Merkert"

from errorrep import UnimplementedMethod
from PyQt4 import QtCore, QtGui
import numpy as np
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


class CircularDisplay (QtGui.QWidget, Display):

    skala_repaint_signal = QtCore.pyqtSignal()

    def __init__(self, name, interval, unit, parent = None):
        QtGui.QWidget.__init__(self, parent = parent)
        Display.__init__(self, name, interval, unit)
        self._value = 0
        self.setupLocks()
        self.def_calc_angle()
        self.setupUi()
        self.skala_repaint_signal.connect(self.setupSkala)

    def setupLocks(self):
        self.lock_value = QtCore.QReadWriteLock()
        self.lock_bounds = QtCore.QReadWriteLock()
        self.lock_skala = QtCore.QReadWriteLock()
        self.lock_calc_angle = QtCore.QReadWriteLock()


    def put(self, data):
        self.lock_value.lockForWrite()
        Display.put(self, data)
        self.lock_value.unlock()
        # Benachrichtigung zum Neuzeichnen
        self.update()

    def recalc_bounds(self, data):
        self.lock_bounds.lockForWrite()
        Display.recalc_bounds(self, data)
        self.lock_bounds.unlock()
        # Passe bei Aenderung die Winkelberechnung und die Skala an
        self.def_calc_angle()
        # setupSkala() sollte nur aus dem GUI-Thread aus aufgerufen werden
        self.skala_repaint_signal.emit()
    
    def setupUi(self, radius = 150):
        # Radius der Anzeige
        self.radius = radius
        self.setWindowTitle("Circular Display")
        # Erzeuge die Hintegrundelemente
        self.background = self.make_pixmap()
        self.paint_helper(self.background,
                          [self.drawDisk,
                           self.drawLabels])
        # Stelle sicher, dass alle pixmaps gefuellt sind.
        self.skala = self.background
        # Erzeuge den Zeiger
        self.notch = self.make_pixmap()
        self.paint_helper(self.notch, [self.drawNotch])
        self.setupSkala()


    @QtCore.pyqtSlot()
    def setupSkala(self):
        pm = self.make_pixmap()
        self.paint_helper(self.skala,
                          [self.drawTicks])
        self.lock_skala.lockForWrite()
        self.skala = pm
        self.lock_skala.unlock()

    def make_pixmap(self):
        pm = QtGui.QPixmap(2 * self.radius, 2 * self.radius)
        pm.fill(QtCore.Qt.transparent)
        return pm
        
    def paint_helper(self, target, funs):
        painter = QtGui.QPainter()
        painter.begin(target)
        # Aktiviere Antialiasing
        painter.setRenderHint(QtGui.QPainter.Antialiasing, True)
        painter.setRenderHint(QtGui.QPainter.TextAntialiasing, True)
        # Aendere Koordinaten
        painter.translate(self.radius, self.radius)
        # Male
        for f in funs:
            f(painter)
        # Ende
        painter.end()

    # Sorge dafuer, dass das Widget gross genug dargestellt wird
    def sizeHint(self):
        return QtCore.QSize(2 * self.radius, 2 * self.radius)

    def minimumSizeHint(self):
        return QtCore.QSize(2 * self.radius, 2 * self.radius)

    def paintEvent_old(self, event):
        self.paint_helper(self,
                          [self.drawDisk,
                           self.drawTicks,
                           self.drawLabels,
                           self.drawIndicator,
                           self.drawNotch])

    def paintEvent(self, event):
        painter = QtGui.QPainter()
        painter.begin(self)
        painter.setCompositionMode(QtGui.QPainter.CompositionMode_SourceOver)
        # Male die Pixmaps
        painter.drawPixmap(0, 0, self.background)
        self.lock_skala.lockForRead()
        painter.drawPixmap(0, 0, self.skala)
        self.lock_skala.unlock()
        # Aendere Koordinaten
        painter.translate(self.radius, self.radius)
        # Zeichne Zeiger -- fuer Performance kein Antialias
        self.drawIndicator(painter)
        # Aendere Koordinaten zurueck
        painter.translate(-self.radius, -self.radius)
        painter.drawPixmap(0, 0, self.notch)
        painter.end()    


    def drawDisk(self, pa):
        bg = select_color("background")
        ri = select_color("ridge")
        pa.setBrush(bg)
        ridge_strength = 5
        pen = QtGui.QPen(ri, ridge_strength, QtCore.Qt.SolidLine)
        pa.setPen(pen)
        diam = 2 * (self.radius - ridge_strength)
        offset = -self.radius + ridge_strength
        pa.drawEllipse(offset, offset, # Ecke
                       diam, diam) # Breite, Hoehe

    def drawNotch(self, pa):
        fg = select_color("foreground")
        ri = select_color("ridge")
        pa.setBrush(fg)
        pen = QtGui.QPen(ri, 3, QtCore.Qt.SolidLine)
        pa.setPen(pen)
        offset = 0.13 * self.radius
        pa.drawEllipse(-offset, -offset, # Ecke
                       2 * offset, 2 * offset) # Breite, Hoehe

    def drawTicks(self, pa, nr = 11):
        # Berechne die Positionen fuer die gewuenschte Anzahl von
        # Markierungen
        angles = np.linspace(0.1 * 2*np.pi, 0.9 * 2*np.pi, nr)
        self.lock_bounds.lockForRead()
        labels = np.linspace(self.get_lower(), self.get_upper(), nr)
        self.lock_bounds.unlock()
        x_pos = - np.sin(angles)
        y_pos = - np.cos(angles)
        # Bestimme Positionen fuer Anfang/Ende der Striche und
        # Beschriftungen
        def scale_and_transform(x, y, scaling):
            return (scaling * self.radius * x,
                    -scaling * self.radius * y)
        start_x, start_y = scale_and_transform(x_pos, y_pos, 0.8)
        end_x, end_y     = scale_and_transform(x_pos, y_pos, 0.9)
        label_x, label_y = scale_and_transform(x_pos, y_pos, 0.7)
                       
        # Zeichne die Striche
        ti = select_color("ticks")
        # pa.setBrush(None)
        pen = QtGui.QPen(ti, 4, QtCore.Qt.SolidLine)
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
        if len(self._unit) > 0:
            pa.drawText(-50, 0.75 * self.radius - 20, 100, 40,
                        QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter,
                        "[%s]" % self._unit)
        pa.setFont(select_font(16))
        if len(self._name) > 0:
            pa.drawText(-50, 0.4 * self.radius - 15, 100, 30,
                        QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter,
                        self._name)

    def def_calc_angle(self):
        # Vollkreis
        vk = 2 * np.pi
        # Rechne den Winkel
        self.lock_bounds.lockForRead()
        l, u = self.get_lower(), self.get_upper()
        self.lock_bounds.unlock()
        la, ua = 0.1 *vk, 0.9 *vk
        try:
            s = (ua - la) / (u - l)
        except ZeroDivisionError:
            s = 1
        self.lock_calc_angle.lockForWrite()
        self.calc_angle = lambda value: (value - l) * s  + la
        self.lock_calc_angle.unlock()
    
    def drawIndicator(self, pa, angle = None):
        # Normalerweise wird der Winkel berechnet
        if angle == None:
            self.lock_value.lockForRead()
            self.lock_calc_angle.lockForRead()
            angle = self.calc_angle(self._value) # * np.pi / 180
            self.lock_calc_angle.unlock()
            self.lock_value.unlock()
        # Berechne die Punkte des Zeigers
        all_angles = np.array([angle - np.pi/2, angle, angle + np.pi/2, angle + np.pi])
        # Rechne die Position
        scales = self.radius * np.array([0.1, 0.75, 0.1, 0.2])
        x_pos, y_pos = (scales * (- np.sin(all_angles)),
                        -scales * (- np.cos(all_angles)))
        # Fuellfarbe
        ind = select_color("indicator")
        pa.setBrush(ind)
        pa.setOpacity(0.8)
        # Zeichne den Zeiger
        indicator = QtGui.QPolygonF([QtCore.QPointF(x,y) for x,y in zip(x_pos, y_pos)])
        pa.drawPolygon(indicator)
        pa.setOpacity(1)

MeterStack.register("circular", CircularDisplay)

def bsp():
    w = CircularDisplay(name="Drehzahl", interval="dynamic", unit="rpm")
    w.show()
    return w

# BUG Skala wird nicht richtig aktualisiert
