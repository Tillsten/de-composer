#!/usr/bin/epython

import sys
import os.path
sys.path.append(os.path.dirname(os.path.realpath(__file__)))

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

if __name__ == "__main__":
    print "This is a module for moving average bins."
