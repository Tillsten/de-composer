#!/usr/bin/epython

import sys
import os.path
sys.path.append(os.path.dirname(os.path.realpath(__file__)))
from math import e,sqrt,pi

def sbin(xs, sz):
    if sz <= 0 or len(xs) < sz:
        raise Exception("not enough data to bin.")
    
    bs = []
    for start in range(len(xs) - sz + 1):
        end = start + sz
        bs.append(sum(xs[start:end]))
    
    return bs

def abin(xs, sz):
    bs = sbin(xs, sz)
    return map(lambda x: x / float(sz), bs)

def tc_kernel(d, w):
    """Tricubic kernel defined by distance from centre and kernel width.
       \left( 1 - (\frac {x-x_o} {w})^3 \right)^3
       \mid d = x-x_o \forall x \in [x_o - w, x_o + w]"""
    d = float(abs(d))
    w = float(w)
    return max(0, (1 - (d/w)**3)**3)

def gs_kernel(d, sd):
    """Kernel defined by the normalized Gaussian function:
       \frac{1}{\delta\sqrt{}{2\pi}} e^{-\frac{d^2}{2*\delta{}^2}}
       Defined by the standard deviation and distance."""
    sd = float(sd)
    d = float(d)
    
    a = 1./(sd * sqrt(2*pi))
    b = -0.5 * (d / sd)**2
    return a * e**(b)

if __name__ == "__main__":
    print "This is a module for moving average bins."
