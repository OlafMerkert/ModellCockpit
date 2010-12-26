#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division

__author__ = "Olaf Merkert"


def rescale_positive(x):
    """Skaliere eine Achse vom Bereich [-1, 1] auf den Bereich [0, 1]"""
    return (x + 1) / 2

def max_mix(neg, pos):
    """Mische zwei Achsen, wobei immer die mit dem hoeheren Wert
    gewinnt.  Als zusaetzliche Rueckgabe bekommt man -1, falls die
    neg-Achse gewinnt, andernfalls +1."""
    if neg > pos:
        return (neg, -1)
    else:
        return (pos, +1)

def diff_mix(neg, pos):
    """Mische zwei Achsen, indem man einfach die Differenz nimmt und
    danach wieder normiert."""
    return (pos - neg) / 2

def deadzone(x, d):
    """Fuehre eine Deadzone in [-d, d] um 0 ein und skaliere so, dass
    voller Schub noch erreicht werden kann."""
    y = abs(x)
    if y > d:
        y = (y - d) / (1 - d)
    else:
        y = 0
    if x < 0:
        return -y
    else:
        return y

def sign(x):
    "Extrahiere das Vorzeichen einer Zahl."
    if x > 0:
        return 1
    elif x < 0:
        return -1
    else:
        return 0
