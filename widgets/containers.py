#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = "Olaf Merkert"

from PyQt4 import QtCore, QtGui
import common

class MeterStack (QtGui.QWidget, common.DataCollection):
    
    # Signal zum Erzeugen eines neuen Moduls
    create_module_signal = QtCore.pyqtSignal(str)

    def __init__(self, parent = None):
        QtGui.QWidget.__init__(self, parent = parent)
        common.DataCollection.__init__(self)
        # Wir ordnen die Anzeigen vertikal an
        self.layout = QtGui.QVBoxLayout()
        self.setLayout(self.layout)
        # self.setMinimumSize( 600, 100 )
        
        self.create_module_signal.connect(self.create_module_slot,
                                          type=QtCore.Qt.QueuedConnection)
        self._ready = QtCore.QWaitCondition()
        self._mutex = QtCore.QMutex()

    @QtCore.pyqtSlot(str)
    def create_module_slot(self, name):
        name = str(name)
        cls = self.find_cls(name)
        m = cls(name)
        self.layout.addWidget(m)
        self._modules[name] = m
        self._ready.wakeAll()
        # return m

    def create_module(self, name):
        self._mutex.lock()
        self.create_module_signal.emit(name)
        self._ready.wait(self._mutex)
        self._mutex.unlock()

def test_container():
    m = MeterStack()
    m.show()
    m.put("Drehzahl", 300)
    m.put("Spannung", 2.3)
    return m
