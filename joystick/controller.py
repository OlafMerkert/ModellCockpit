#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division

__author__ = "Olaf Merkert"

from errorrep import JoystickNotFound, UnimplementedMethod
from thread_helpers import Loop, Abort

# Lade und initialisiere Pygame Joystick Modul
import pygame
from pygame.joystick import get_count as js_count, Joystick as js_Joystick
pygame.init()

# Erlaube nur Joystickbuttons und Hat-Switches als Event-Quellen
# (sowie eigene Events).  Theoretisch waere es eleganter, set_allowed
# zu verwenden, aber das scheint nicht zu funktionieren.
pygame.event.set_blocked([
    pygame.QUIT,
    pygame.ACTIVEEVENT,
    pygame.KEYDOWN,
    pygame.KEYUP,
    pygame.MOUSEMOTION,
    pygame.MOUSEBUTTONUP,
    pygame.MOUSEBUTTONDOWN,
    pygame.JOYAXISMOTION,
    pygame.JOYBALLMOTION,
#    pygame.JOYHATMOTION,
    pygame.JOYBUTTONUP,
#    pygame.JOYBUTTONDOWN,
    pygame.VIDEORESIZE,
    pygame.VIDEOEXPOSE,
#    pygame.USEREVENT,
])

# TODO Kalibrationsverfahren

# Finden von Joysticks
def find_joystick(id_or_name):
    nr = js_count() # Anzahl der vorhandenen Joysticks
    if isinstance(id_or_name, str): # Substring-Suche
        for i in xrange(nr):
            j = js_Joystick(i)
            if id_or_name.lower() in j.get_name().lower():
                return j
    elif isinstance(id_or_name, int) \
             and (0 <= id_or_name < nr): # Id-Suche
        return js_Joystick(id_or_name)
    else:
        raise JoystickNotFound(id_or_name)

class Joystick (object):

    def __init__(self, id_or_name = 0):
        self._device = find_joystick(id_or_name)
        self._device.init()
        self._id = self._device.get_id()
        # self._num = (self._device.get_numaxes(),
        #              self._device.get_numhats(),
        #              self._device.get_numbuttons())


    def __del__(self):
        self._device.quit()

    def name(self):
        return self._device.get_name()

    def a(self, nr):
        return self._device.get_axis(nr)

    def calibrate_helper(self, axes, tolerance=0.05):
        maxes = list(axes)
        mines = list(axes)
        M = 1 - tolerance
        m = - M
        def loop_fun():
            # Eingabe holen
            pygame.event.pump()
            if len(maxes) + len(mines) > 0:
                # Warte auf maximale Auslenkung
                for i, a in enumerate(maxes):
                    if self.a(a) >= M:
                        del maxes[i]
                        break
                # Warte auf minimale Auslenkung
                for i, a in enumerate(mines):
                    if self.a(a) <= m:
                        del mines[i]
                        break
            else:
                raise Abort()
        # return loop_fun
        return Loop(loop_fun)

    def calibrate(self):
        raise UnimplementedMethod()


    def handle_next_event(self):
        """Schaue nach, ob ein Event vorliegt.  Falls ja, verarbeite
        und gebe False zurueck.  Sonst True."""
        ev = pygame.event.poll()
        # Button event
        if ev.type == pygame.JOYBUTTONDOWN:
            # Teste, ob das Event von diesem Joystick kommt
            if ev.joy == self._id:
                self.handle_button(ev.button)
                return True
        # Hat event
        elif ev.type == pygame.JOYHATMOTION:
            # Teste, ob das Event von diesem Joystick kommt
            if ev.joy == self._id:
                self.handle_hat(ev.hat, ev.value)
                return True
        # Leere Event Queue oder falsches Event
        return False

    def handle_button(self, nr):
        pass

    def handle_hat(self, nr, dir):
        pass

    def next_command(self):
        if not self.handle_next_event():
            # Geraeteeingabe holen
            pygame.event.pump()
            self.send()

    def send(self):
        raise UnimplementedMethod

    def send_loop(self):
        l = Loop(self.next_command)
        # l.setDaemon(True)
        return l


class Steuerung (object):

    def __init__(self, cmdr):
        self._commander = cmdr

    @classmethod
    def create(cls, cmdr):
        """Automatische Auswahl des Controllers anhand des
        erforderlichen Typs."""
        c = cls.profiles[cmdr.fahrzeug_typ()]
        return c(cmdr)

    def axis_data(self):
        raise UnimplementedMethod


class Steuerung_A (Steuerung):

    def send(self):
        data = self.axis_data()
        self._commander.steuern_A(*data)

class Steuerung_P (Steuerung):

    def send(self):
        data = self.axis_data()
        self._commander.steuern_P(*data)

class Steuerung_F (Steuerung):

    def send(self):
        data = self.axis_data()
        self._commander.steuern_F(*data)

class Steuerung_H (Steuerung):

    def send(self):
        data = self.axis_data()
        self._commander.steuern_H(*data)
