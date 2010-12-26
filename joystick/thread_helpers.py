#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = "Olaf Merkert"

import pygame
pygame.init()
from threading import Thread, Timer, Event

class Abort (Exception):
    pass

class StoppableThread (Thread):
    """Eine einfache Erweiterung von Thread, damit man den Thread auch
    gut stoppen kann."""

    def __init__(self, *args, **kwargs):
        Thread.__init__(self, *args, **kwargs)
        self._stop = Event()

    def stop(self):
        self._stop.set()

    def is_stopped(self):
        return self._stop.isSet()


class Loop (StoppableThread):
    """Eine einfache Klasse, um eine Funktion wieder und
    wieder aufzurufen."""

    def __init__(self, fn):
        StoppableThread.__init__(self)
        self._fn = fn

    def run(self):
        try:
            while not self.is_stopped():
                self._fn()
        except Abort:
            pass

class PygameLoop (Loop):

    def stop(self):
        StoppableThread.stop(self)
        pygame.event.post(
            pygame.event.Event(pygame.USEREVENT, joy=0))

class TimedLoop (StoppableThread):
    """Eine einfache Klasse, um eine Funktion in regelmaessigen
    Zeitintervallen wieder und wieder aufzurufen."""

    def __init__(self, fn, interval = 0.1):
        StoppableThread.__init__(self)
        self._fn = fn
        self._interval = interval

    def run(self):
        try:
            while not self.is_stopped():
                t = Timer(self._interval, self._fn)
                t.start()
        except Abort:
            pass
