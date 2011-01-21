#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = "Olaf Merkert"

from errorrep import UnimplementedMethod


class Commander (object):

    def kamera(self, x, y):
        """Richte die Kamera aus.  x,y aus dem Intervall [-1,1]."""
        pass

    def fahrzeug_typ(self):
        """Rueckgabe: A, P, F oder H fuer Auto, Pistenbully, Flugzeug
        oder Hubschrauber."""
        raise UnimplementedMethod

    # def steuern(self, *args):
    #     """Sende Steuerdaten an das Fahrzeug."""
    #     fns = {
    #         "A" : self.steuern_A,
    #         "P" : self.steuern_P,
    #         "F" : self.steuern_F,
    #         "H" : self.steuern_H,
    #         }
    #     return fns[self.fahrzeug_typ()](*args)


class AutoCommander (Commander):

    def fahrzeug_typ(self):
        return "A"

    def steuern_A(self, gas, lenkung):
        """Setze Gas und Lenkausschlag, beide sollten
        zwischen -1 und 1 liegen.  Dabei heisst 1 vorwärts
        bzw. rechts."""
        pass

class PibuCommander (Commander):

    def fahrzeug_typ(self):
        return "P"

    def steuern_P(self, gas, lenkung, gang):
        """Setze Gas, Gang und Lenkausschlag.  Gas ist zwischen 0 und
        1, 1 fuer Vollgas.  Gang ist eines von -1, 0, 1, dabei ist 1
        vorwärts und 0 Leerlauf.  Lenkausschlag ist zwischen -1 und 1,
        1 heisst rechts."""
        # TODO Im Leerlauf sollte es eine Beschränkung des Gases geben
        pass

    def motor_aus(self):
        """Schalte den Motor ab."""
        pass

class FlugzeugCommander (Commander):

    def fahrzeug_typ(self):
        return "F"

    def steuern_F(self, schub, seitenruder, querruder, hoehenruder):
        pass

class HeliCommander (Commander):

    def fahrzeug_typ(self):
        return "H"

    def steuern_H(self, kollektiv, ruder, zyklisch_x, zyklisch_y):
        pass

    def motor_aus(self):
        """Schalte den Motor ab."""
        pass

    
