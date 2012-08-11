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

def tc_bin(xs, w):
    """Applies the following kernel, steeper than the gaussian:
       \left( 1 - (\frac {x-x_o} {w})^3 \right)^3
       \forall x \in [x_o - w, x_o + w]"""
    bs = []
    for i in range(len(xs)):
        start = max(0, i-w)
        end = min(len(xs), i+w+1)
        
        subl = xs[start:end]
        idxs = [i+idx for idx in range(len(subl))]
        
        kerneld = [tc_kernel(p[0]-i, w) * p[1] for p in zip(idxs,subl)]
        norm = sum([tc_kernel(idx-i, w) for idx in idxs])
        bs.append(sum(kerneld)/norm)
        print norm
    return bs

def tc_kernel(d, w):
    """Need: distance from centre and kernel width."""
    d = float(abs(d))
    w = float(w)
    return max(0, (1 - (d/w)**3)**3)

def gs_bin(xs, sd):
    """Applies a gaussian kernel to the bins, preferentially weights
       local samples and deprecates distant sample"""
    if sd <= 0:
        raise Exception("Gaussian convolution requires positive nonzero SD.")
    
    w = 5 * sd
    bs = []
    for i in range(len(xs)):
        start = int(max(0, i-w))
        end = int(min(len(xs), i+w+1))
        
        subl = xs[start:end]
        idxs = [i+idx for idx in range(len(subl))]
        
        kerneld = [gs_kernel(p[0]-i, sd) * p[1] for p in zip(idxs,subl)]
        bs.append(sum(kerneld))
    return bs

def gs_kernel(d, sd):
    """Defined by the standard deviation and distance."""
    sd = float(sd)
    d = float(d)
    
    a = 1./(sd * sqrt(2*pi))
    b = -0.5 * (d / sd)**2
    return a * e**(b)

if __name__ == "__main__":
    print "This is a module for moving average bins."
