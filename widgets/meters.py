#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = "Olaf Merkert"

from errorrep import UnimplementedMethod
import common
from PyQt4 import QtCore, QtGui

# TODO leere die Liste der registrierten Module
common.reset_cockpit_modules()

class AbstractMeter (QtGui.QWidget, common.NumericData):

    def __init__(self, name, parent = None):
        self._name = name
        QtGui.QWidget.__init__(self, parent)
        self.setupUi()
        common.NumericData.__init__(self)

    def setupUi():
        raise UnimplementedMethod

    def setup_units(self, units):
        # Breite in Pixel fuer die Labels mit den Einheiten
        units.setMinimumWidth(40)
        units.setMaximumWidth(40)

    def setup_dig(self, dig):
        self.dig.setSegmentStyle(QtGui.QLCDNumber.Filled)
        self.dig.setDigitCount(7)
        self.dig.setMinimumSize(7 * 20, 30)
        self.dig.setFrameStyle(QtGui.QFrame.NoFrame)


# Drehzahlanzeige
class DrehzahlMeter (AbstractMeter):

    def setupUi(self):
        # Erzeuge die Komponenten
        label = QtGui.QLabel(self._name)
        self.dial = QtGui.QDial()
        self.dig = QtGui.QLCDNumber()
        units = QtGui.QLabel("[ rpm ]")
        # Konfiguriere die Anzeigen
        self.dial.setEnabled(False)
        self.dial.setNotchesVisible(True)
        self.dial.setMinimumSize( 100, 100 )
        self.setup_units(units)
        self.setup_dig(self.dig)

        self.setMinimumHeight( 100 + 5 )

        # Anordnen
        layout = QtGui.QHBoxLayout(self)
        layout.addWidget(label)
        layout.addStretch(1)
        layout.addWidget(self.dial)
        layout.addWidget(self.dig)
        layout.addWidget(units)


    def _update(self):
        self.dial.setValue(self._value)
        self.dial.valueChanged.emit(self._value)
        self.dig.display(self._value)

    def _update_bounds(self):
        self.dial.setMinimum(self._min)
        self.dial.setMaximum(self._max)
        self.dial.rangeChanged.emit(self._min, self._max)

common.register_cockpit_module(
    DrehzahlMeter,
    ["drehzahl", "umdreh", "rpm"])

# Spannungsanzeige
class VoltMeter (AbstractMeter):

    def setupUi(self):
        # Erzeuge die Komponenten
        label = QtGui.QLabel(self._name)
        self.slider = QtGui.QSlider(QtCore.Qt.Horizontal)
        self.dig = QtGui.QLCDNumber()
        units = QtGui.QLabel("[ V ]")
        # Konfiguriere die Anzeigen
        self.slider.setEnabled(False)
        self.slider.setMinimumWidth(150)
        self.slider.setMaximumWidth(250)
        self.setup_units(units)
        self.setup_dig(self.dig)

        self.setMinimumHeight( 40 + 5 )

        # Anordnen
        layout = QtGui.QHBoxLayout(self)
        layout.addWidget(label)
        layout.addStretch(1)
        layout.addWidget(self.slider)
        layout.addWidget(self.dig)
        layout.addWidget(units)



    def _update(self):
        self.slider.setValue(self._value)
        self.slider.valueChanged.emit(self._value)
        self.dig.display(self._value)

    def _update_bounds(self):
        self.slider.setMinimum(self._min)
        self.slider.setMaximum(self._max)
        self.slider.rangeChanged.emit(self._min, self._max)

common.register_cockpit_module(
    VoltMeter,
    ["volt", "spannung"])

# Temperaturanzeige
class ThermoMeter (AbstractMeter):

    def setupUi(self):
        # Erzeuge die Komponenten
        label = QtGui.QLabel(self._name)
        self.slider = QtGui.QSlider(QtCore.Qt.Horizontal)
        self.dig = QtGui.QLCDNumber()
        units = QtGui.QLabel("[ deg C ]")
        # Konfiguriere die Anzeigen
        self.slider.setEnabled(False)
        self.slider.setMinimumWidth(150)
        self.slider.setMaximumWidth(250)
        self.setup_units(units)
        self.setup_dig(self.dig)

        self.setMinimumHeight( 40 + 5 )

        # Anordnen
        layout = QtGui.QHBoxLayout(self)
        layout.addWidget(label)
        layout.addStretch(1)
        layout.addWidget(self.slider)
        layout.addWidget(self.dig)
        layout.addWidget(units)



    def _update(self):
        self.slider.setValue(self._value)
        self.slider.valueChanged.emit(self._value)
        self.dig.display(self._value)

    def _update_bounds(self):
        self.slider.setMinimum(self._min)
        self.slider.setMaximum(self._max)
        self.slider.rangeChanged.emit(self._min, self._max)

common.register_cockpit_module(
    ThermoMeter,
    ["temp", "thermo"])
