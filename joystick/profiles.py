#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = "Olaf Merkert"

from transforms import rescale_positive, diff_mix, deadzone, sign
from controller import Joystick, Steuerung, Steuerung_A, Steuerung_P, Steuerung_F, Steuerung_H

# ==============================================================================
# Konfiguration X-Box Controller

class XBoxController (Joystick, Steuerung):
    profiles = {}

    def __init__(self, cmdr):
        Joystick.__init__(self, "X-Box")
        Steuerung.__init__(self, cmdr)

class XBoxController_A (XBoxController, Steuerung_A):

    def axis_data(self):
        # Gas
        gas = diff_mix( self.a(2), self.a(5) )
        lenkung = self.a(0)
        return (gas, lenkung)

XBoxController.profiles["A"] = XBoxController_A

class XBoxController_P (XBoxController, Steuerung_P):

    def axis_data(self):
        # Gas und Gangschaltung
        gas = deadzone(diff_mix( self.a(2), self.a(5) ), 0.05)
        gang = sign(gas)
        gas = abs(gas)
        # Lenkung
        lenkung = self.a(0)
        return (gas, lenkung, gang)

    def handle_button(self, nr):
        if nr == 7:
            self._commander.motor_aus()

XBoxController.profiles["P"] = XBoxController_P
