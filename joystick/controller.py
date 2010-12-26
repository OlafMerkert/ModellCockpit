#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division

__author__ = "Olaf Merkert"

from errorrep import JoystickNotFound
from thread_helpers import Loop, PygameLoop

# Lade und initialisiere Pygame Joystick Modul
import pygame
from pygame.joystick import get_count as js_count, Joystick as js_Joystick
pygame.init()

# Erlaube nur Joystickbuttons und Hat-Switches als Event-Quellen
# (sowie eigene Events)
pygame.event.set_allowed([
    pygame.JOYBUTTONDOWN,
    pygame.JOYHATMOTION,
    pygame.USEREVENT,
    ])
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
#    pygame.JOYBUTTONUP,
    pygame.JOYBUTTONDOWN,
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

    def handle_next_event(self):
        ev = pygame.event.wait()
        # Teste zuerst, ob das Event von diesem Joystick kommt
        if ev.joy == self._id:
            # Button event
            if ev.type == pygame.JOYBUTTONDOWN:
                self.handle_button(ev.button)
            # Hat event
            elif ev.type == pygame.JOYHATMOTION:
                self.handle_hat(ev.hat, ev.value)

    def handle_button(nr):
        pass

    def handle_hat(nr, dir):
        pass

    def run_event_loop(self):
        l = PygameLoop(self.handle_next_event)
        # l.setDaemon(True)
        l.start()
        # NOTE Threadreferenz speichern?
        return l

# TODO Fasse die beiden Threads zu einem einzigen zusammen

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

    def run_send_loop(self):
        l = Loop(self.send)
        # l.setDaemon(True)
        l.start()
        # NOTE Threadreferenz speichern
        return l

class Steuerung_A (Steuerung):

    def send(self):
        # regelmaessig die Event-Queue bearbeiten
        pygame.event.pump()
        data = self.axis_data()
        self._commander.steuern_A(*data)

class Steuerung_P (Steuerung):

    def send(self):
        # regelmaessig die Event-Queue bearbeiten
        pygame.event.pump()
        data = self.axis_data()
        self._commander.steuern_P(*data)

class Steuerung_F (Steuerung):

    def send(self):
        # regelmaessig die Event-Queue bearbeiten
        pygame.event.pump()
        data = self.axis_data()
        self._commander.steuern_F(*data)

class Steuerung_H (Steuerung):

    def send(self):
        # regelmaessig die Event-Queue bearbeiten
        pygame.event.pump()
        data = self.axis_data()
        self._commander.steuern_H(*data)

