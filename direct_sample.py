#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = "Olaf Merkert"

import widgets
import joystick

from joystick.commands import PibuCommander
from widgets.containers import MeterStack
from joystick.profiles import XBoxController

import sys
import time
from PyQt4 import QtGui

class GuiPibu (MeterStack, PibuCommander):

    def __init__(self):
        MeterStack.__init__(self)

    def steuern_P(self, gas, lenkung, gang):
        print "Gas: %f,  Lenkung: %f,  Gang: %d" % (gas, lenkung, gang)
        # schicke die Daten an die GUI
        self.put("Drehzahl", gas * 1000)
        self.put("Lenkung //rpm", lenkung)
        self.put("Gang //volt", gang)
        # warte ein bisschen
        time.sleep(0.01)

    def motor_aus(self):
        print "|| Motor ausgeschaltet. || ******************************"

def main():
    app = QtGui.QApplication([])
    gp = GuiPibu()
    js = XBoxController.create(gp)

    gp.show()

    l = [js.run_event_loop(),
         js.run_send_loop()]
    # BUG Qt Oberflaeche ist noch nicht am laufen -> Problem
    s = app.exec_()
    # Terminiere die beiden Loops
    for t in l:
        t.stop()
        t.join()
    sys.exit(s)

if __name__=="__main__":
    main()
