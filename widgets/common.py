#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = "Olaf Merkert"

from errorrep import UnknownDisplayException, UnimplementedMethod
from math import log, ceil, floor
from PyQt4 import QtCore
import time

class Data (object):

    def put(self, value):
        "Liefere einen neuen Wert fuer die Anzeige."
        raise UnimplementedMethod


def next_dimension(n):
    """Hilfsfunktion zum Skalieren der Anzeigen.  Runde von 0 weg zu
    der naechsten Zahl, die hoechsten eine Ziffer verschieden von 0
    hat.  Bspp: 120 -> 200; -12 -> -20."""
    # 0 bleibt 0
    if n == 0:
        return n
    m = abs(n)
    # bestimme die Groessenordnung
    o = 10 ** floor( log(m, 10) )
    # Runde in dieser Groessenordnung auf
    r = o * ceil(m/o)
    # Zum Schluss passe das Vorzeichen an
    if n < 0:
        return -r
    else:
        return r

class NumericData (Data):

    def __init__(self):
        # Setze Grenzen und uebernehme
        self._min = 0
        self._max = 0
        self._update_bounds()
        # Setze Wert
        self._value = 0
        self._update()

    def put(self, value, calib = False):
        """Nehme einen neuen Wert entgegen.  Falls gewuenscht, passe
        automatisch Grenzen an (d.h. rufe update_bounds() auf)."""
        if calib:
            self.update_bounds(value)
        self._value = value
        self._update()

    def _update(self):
        """Wird automatisch bei Wertaenderungen aufgerufen."""
        pass

    def update_bounds(self, value):
        """Pruefe, ob der Wert sich noch in den vorgegebenen Grenzen
        bewegt.  Falls nicht, passe die Grenzen entsprechend an."""
        m,M = False, False
        # Teste, ob Maximum ueberschritten wurde
        if value > self._max:
            self._max = next_dimension(value)
            M = True
        # Teste, ob Minimum ueberschritten wurde
        if value < self._min:
            self._min = next_dimension(value)
            m = True
        # Falls ja, aktualisiere die Anzeige
        if m or M:
            self._update_bounds()
        return (m,M)

    def _update_bounds():
        """Wird automatisch bei Aenderung der Grenzen aufgerufen."""
        pass

class DataCollection (QtCore.QObject):
    cockpit_modules = []
    # update_freq = 5

    def __init__(self):
        self._modules = {}
        self._transformations = {}

    def has_module(self, name):
        return (name in self._modules)

    def put(self, name, value):
        """Zeige einen Wert auf dem passenden Cockpitelement an.  Bei
        Bedarf wird eine Anzeige neu erzeugt."""
        if self.has_module(name):
            self._modules[name].put(value, True)
        else:
            self.create_module(name)
            if self.has_module(name):
                self._modules[name].put(value, True)

    def tput(self, name, value):
        """Wie put(), aber falls eine Transformation gewuenscht wurde,
        wird diese zuerst angewendet."""
        if name in self._transformations:
            value = self._transformations[name](value)
        self.put(name, value)

    def define_transformation(self, name, fn):
        """Registriere eine Transformation fuer die Anzeige mit
        gegebenen Namen.  Die Funktion sollte als einzigen Parameter
        den vorigen Wert annehmen und als Rueckgabe den neuen Wert
        liefern."""
        self._transformations[name] = fn


    @classmethod
    def find_cls(c, name):
        """Durchsuche die Liste der Module nach Stichwoertern, die in
        name enthalten sind.  Die Suche geschieht ohne
        Beruecksichtigung der Gross/Kleinschreibung und liefert als
        Ergebnis eine Klasse."""
        # Alle Stichwoerter sollen kleingeschrieben sein
        iname = name.lower()
        for keys, cls in DataCollection.cockpit_modules:
            if key_match(iname, keys):
                return cls
        raise UnknownDisplayException(name)

    def create_module(self, name):
        """Diese Methode wird aufgerufen, wenn eine neue Anzeige
        erstellt werden muss."""
        raise UnimplementedMethod

def sometimes(n):
    """Erzeuge eine Funktion, die bei jedem n-ten Aufruf True
    zurueckgibt, sonst aber immer False."""
    x = [-1]
    def c():
        x[0] += 1
        return (x[0] % n == 0)
    return c

def key_match(s, keys):
    return any([(k in s) for k in keys])

def register_cockpit_module(cls, keywords=[], type="meter"):
    """Melde ein Modul an.  Die keywords sollten eine Liste von
    kleingeschriebenen Strings sein."""
    DataCollection.cockpit_modules.append((keywords, cls))

def reset_cockpit_modules():
    "Loesche alle zuvor registrierten Module."
    DataCollection.cockpit_modules = []
