#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = "Olaf Merkert"

import joystick
import displays

from joystick.commands import PibuCommander
from joystick.profiles import XBoxController
from displays.terminal_out import MeterStack

import time

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

        self.motor_status = self.create_display(
            name="Motor Aus",
            type="light",
            )


    def steuern_P(self, gas, lenkung, gang):
        self.gas.put(gas * 1000)
        self.lenkung.put(lenkung)
        self.gang.put(gang)
        # warte kurz
        # time.sleep(0.01)

    def motor_aus(self):
        self.motor_status.put(1)


def main():
    pd = PibuDisplays()
    js = XBoxController.create(pd)

    pd.show()

    l = js.send_loop()
    l.start()
    l.wait()

if __name__=="__main__":
    main()
