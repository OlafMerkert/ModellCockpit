#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = "Olaf Merkert"

from PyQt4 import QtGui
import common

class MeterStack (QtGui.QWidget, common.DataCollection):

    def __init__(self, parent = None):
        QtGui.QWidget.__init__(self, parent = parent)
        common.DataCollection.__init__(self)
        # Wir ordnen die Anzeigen vertikal an
        self.layout = QtGui.QVBoxLayout()
        self.setLayout(self.layout)
        # self.setMinimumSize( 600, 100 )

    def create_module(self, name):
        cls = self.find_cls(name)
        m = cls(name)
        self.layout.addWidget(m)
        return m

def test_container():
    m = MeterStack()
    m.show()
    m.put("Drehzahl", 300)
    m.put("Spannung", 2.3)
    return m
