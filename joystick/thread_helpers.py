#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = "Olaf Merkert"

from PyQt4 import QtCore

class Abort (Exception):
    """Werfe diese Exception, um einen Loop abzubrechen."""
    pass

class Loop (QtCore.QThread):
    """Eine einfache Klasse, um eine Funktion wieder und
    wieder aufzurufen."""

    def __init__(self, fn):
        QtCore.QThread.__init__(self)
        self._fn = fn
        self._running = False

    def run(self):
        self._running = True
        try:
            while self._running:
                self._fn()
        except Abort:
            pass

    def is_running(self):
        return self._running

    def stop(self):
        self._running = False
        self.wait()

    def __del__(self):
        self.stop()


class TimedLoop (Loop):
    """Eine einfache Klasse, um eine Funktion in regelmaessigen
    Zeitintervallen wieder und wieder aufzurufen."""

    def __init__(self, fn, interval = 0.1):
        Loop.__init__(self, fn)
        self._interval = interval

    def run(self):
        try:
            while self._running:
                self._fn()
                self.sleep(self._interval)
        except Abort:
            pass
