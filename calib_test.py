#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = "Olaf Merkert"

import joystick
from joystick.profiles import XBoxController

def main():
    js = XBoxController(None)
    print "Beginne Kalibrierung."
    js.calibrate()
    print "Kalibrierung abgeschlossen."

if __name__=="__main__":
    main()
