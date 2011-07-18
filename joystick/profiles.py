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

XBoxController.register("A", XBoxController_A)

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

XBoxController.register("P", XBoxController_P)

# ==============================================================================
# Konfiguration G940

class G940 (Joystick, Steuerung):
    profiles = {}

    def __init__(self, cmdr, id = None):
        if id == None:
            Joystick.__init__(self, "G940")
        else:
            Joystick.__init__(self, id)
        Steuerung.__init__(self, cmdr)

    def calibrate(self):
        lo = self.calibrate_helper([], 0.05)
        lo.start()
        lo.wait()

register_profile("G940", G940)

class G940_F (Steuerung_F, G940):

    def axis_data(self):
        schub = deadzone(diff_mix( self.a(6), 1), 0.05)
        return (schub, self.a(2), self.a(0), self.a(1))

G940.register("F", G940_F)

class G940_H (Steuerung_H, G940):

    def axis_data(self):
        schub = deadzone(diff_mix( -1, self.a(6) ), 0.05)
        return (schub, self.a(2), self.a(0), self.a(1))

    def handle_button(self, nr):
        if nr == 1:
            self._commander.motor_aus()

G940.register("H", G940_H)

# ==============================================================================
# Konfiguration TmHotasX

class TmHotasX (Joystick, Steuerung):
    profiles = {}

    def __init__(self, cmdr, id = None):
        if id == None:
            Joystick.__init__(self, "T.Flight Hotas")
        else:
            Joystick.__init__(self, id)
        Steuerung.__init__(self, cmdr)

    def calibrate(self):
        lo = self.calibrate_helper([], 0.05)
        lo.start()
        lo.wait()

register_profile("Thrustmaster T.Flight Hotas X", TmHotasX)

class TmHotasX_A (Steuerung_A, TmHotasX):

    def axis_data(self):
        return (self.a(2), self.a(0))

TmHotasX.register("A", TmHotasX_A)

class TmHotasX_P (Steuerung_P, TmHotasX):

    def axis_data(self):
        gas = deadzone(self.a(2), 0.05)
        gang = sign(gas)
        gas = abs(gas)
        return (gas, self.a(0), gang)

    def handle_button(self, nr):
        if nr == 1:
            self._commander.motor_aus()

TmHotasX.register("P", TmHotasX_P)

class TmHotasX_F (Steuerung_F, TmHotasX):

    def axis_data(self):
        schub = deadzone(diff_mix( self.a(2), 1), 0.05)
        return (schub, self.a(4), self.a(0), self.a(1))

TmHotasX.register("F", TmHotasX_F)

class TmHotasX_H (Steuerung_H, TmHotasX):

    def axis_data(self):
        schub = deadzone(diff_mix( -1, self.a(2) ), 0.05)
        return (schub, self.a(4), self.a(0), self.a(1))

    def handle_button(self, nr):
        if nr == 1:
            self._commander.motor_aus()

TmHotasX.register("H", TmHotasX_H)

# ==============================================================================
# Konfiguration Driving Force GT

class DrivingForce (Joystick, Steuerung):
    profiles = {}

    def __init__(sef, cmdr, id = None):
        if id == None:
            Joystick.__init__(self, "Driving Force")
        else:
            Joystick.__init__(self, id)
        Steuerung.__init__(self, cmdr)

    # TODO calibration if necessary

# TODO verify joystick device name
register_profile("Driving Force GT", DrivingForce)

class DrivingForce_A (Steuerung_A, DrivingForce):

    def axis_data(self):
        # TODO select correct axes
        gas = self.a(1)
        lenkung = self.a(0)
        return (gas, lenkung)

DrivingForce.register("A", DrivingForce_A)
