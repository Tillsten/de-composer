#!/usr/bin/epython

import sys
import os.path
sys.path.append(os.path.dirname(os.path.realpath(__file__)))

class Counter():
    """Abstract base class. Inherited classes will encapsulate logic
       for identifying signal vs. noise singular values."""
    pass

class MassFractionCounter(Counter):
    """Accepts a simple mass fraction of the singular values."""
    def __init__(self, fraction):
        """Initializes with a mass fraction of singular values to accept."""
        self.fraction = fraction
    
    def count_signals(self, values):
        nsignals = 0
        v_sum = sum(values)
        s_sum = 0.0
        for v in values:
            s_sum += v
            nsignals += 1
            if s_sum / v_sum > self.fraction:
                break
        if nsignals % 2 == 1:
            nsignals += 1
        return nsignals

if __name__ == "__main__":
    print "This is a module for defining Singular Value counters."
