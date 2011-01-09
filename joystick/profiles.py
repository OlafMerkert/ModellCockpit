#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = "Olaf Merkert"

from errorrep import NoMatchingProfile
from transforms import rescale_positive, diff_mix, deadzone, sign
from controller import Joystick, Steuerung, \
     Steuerung_A, Steuerung_P, Steuerung_F, Steuerung_H
from pygame.joystick import get_count as js_count, Joystick as js_Joystick

# Automatisches Verwenden der Profile
profile_map = {}

def register_profile(name, clss):
    profile_map[name] = clss

def find_profile(id):
    js = js_Joystick(id)
    return profile_map[js.get_name()]

def get_joystick_profile(id, cmdr):
    pr = find_profile(id)
    return pr.create(cmdr)

def detect_joystick(cmdr):
    # TODO beruecksichtige Praeferenzen
    for id in xrange(js_count()):
        try:
            js = get_joystick_profile(id, cmdr)
        except KeyError:
            # KeyError passiert entweder beim Nachschlagen in der
            # profile_map oder erst beim Nachschlagen in den profiles
            # der Joystick-Klasse.
            continue
        else:
            print "Benutze `%s' als Joystick." % js.name()
            return js
    # Falls keine Joystick gefunden wurde:
    raise NoMatchingProfile

# ==============================================================================
# Konfiguration X-Box Controller

class XBoxController (Joystick, Steuerung):
    profiles = {}

    def __init__(self, cmdr, id = None):
        if id == None:
            Joystick.__init__(self, "X-Box")
        else:
            Joystick.__init__(self, id)
        Steuerung.__init__(self, cmdr)

    def calibrate(self):
        lo = self.calibrate_helper([2, 5], 0.05)
        lo.start()
        lo.wait()

register_profile("Microsoft X-Box 360 pad", XBoxController)

class XBoxController_A (Steuerung_A, XBoxController):

    def axis_data(self):
        # Gas
        gas = diff_mix( self.a(2), self.a(5) )
        lenkung = self.a(0)
        return (gas, lenkung)

XBoxController.profiles["A"] = XBoxController_A

class XBoxController_P (Steuerung_P, XBoxController):

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
