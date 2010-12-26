#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = "Olaf Merkert"

class UnknownDisplayException (Exception):

    def __init__(self, name):
        self._display_name = name

    def __str__(self):
        return "UnknownDisplay: %s" % self._display_name

class UnimplementedMethod (Exception):
    pass

class JoystickNotFound (Exception):

    def __init__(self, id_or_name):
        self._id_or_name = id_or_name

    def __str__(self):
        if isinstance(self._id_or_name, int):
            return "Invalid Joystick id: %d" % self._id_or_name
        elif isinstance(self._id_or_name, str):
            return "Joystick name not found: %s" % self._id_or_name
        else:
            return "Joystick must be identified by int or str"
