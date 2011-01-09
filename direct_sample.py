#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = "Olaf Merkert"

import joystick
import displays

from joystick.commands import PibuCommander
from joystick.profiles import detect_joystick
from displays.common import MeterStack

from PyQt4 import QtCore, QtGui

import time, sys

class PibuDisplays (MeterStack, PibuCommander):

    def __init__(self):
        MeterStack.__init__(self)
        # Erzeuge die Anzeigen
        self.gas = self.create_display(
            name="Gas",
            type="circular",
            unit="rpm",
            interval="dynamic",
            )

        self.gang = self.create_display(
            name="Gang",
            type="circular",
            interval=[-1,1],
            )

        self.lenkung = self.create_display(
            name="Lenkung",
            type="circular",
            interval="dynamic",
            )

    def steuern_P(self, gas, lenkung, gang):
        self.gas.put(gas * 1000)
        self.lenkung.put(lenkung)
        self.gang.put(gang)
        # warte kurz
        # gibt ausserdem dem QtMainThread Zeit zum Zeichnen
        time.sleep(0.1)

    def motor_aus(self):
        print "** Motor ausschalten."


def main():
    app = QtGui.QApplication(sys.argv)
    pd = PibuDisplays()
    # Joystick erzeugen und kalbibrieren
    js = detect_joystick(pd)
    print "Warte auf Kalibration."
    js.calibrate()
    print "Joystick kalibriert."

    pd.show()

    l = js.send_loop()
    l.start()
    s = app.exec_()
    l.stop()
    sys.exit(s)

if __name__=="__main__":
    main()
