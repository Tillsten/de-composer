#!/usr/bin/epython

import sys
import os.path
import random

sys.path.append(os.path.dirname(os.path.realpath(__file__)))

class Periodic:
    """Generates a composed signal of sinusoids."""
    pass

class Gaussian:
    """Generates gaussian noise time-series."""
    def __init__(self, mean, stdev):
        self.mean = mean
        self.stdev = stdev
    
    def time_series(self, length):
        series = [random.gauss(self.mean, self.stdev) for i in range(length)]
        return series

class Step:
    """Generates time-series of step functions."""
    def __init__(self, amp, per, off, bias, nsr):
        self.amplitude = amp
        self.period = per
        self.offset = off
        self.bias = bias
        self.noise = nsr
    
    def time_series(self, length):
        series = [self._make_value(t) for t in range(length)]
        return series
    
    def _make_value(self, time):
        ttime = time - self.offset
        n_per = int(ttime / self.period)
        if n_per % 2 == 0:
            value = self._high_value()
        else:
            value = self._low_value()
        return value
        
    def _high_value(self):
        signal = self.bias + self.amplitude
        noise = self.noise * self.amplitude * random.gauss(0, 1.0)
        return signal + noise
    
    def _low_value(self):
        signal = self.bias - self.amplitude
        noise = self.noise * self.amplitude * random.gauss(0, 1.0)
        return signal + noise

class Impulse:
    """Generates a periodic impulse time-series."""
    def __init__(self, amp, width, per, bias, nsr):
        self.amplitude = amp
        self.width = width
        self.period = per
        self.bias = bias
        self.noise = nsr
        
    def time_series(self, length):
        series = [self._get_value(t) for t in range(length)]
        return series
    
    def _get_value(self, time):
        partial = time % self.period
        dist = abs(partial - self.period)
        frac = max(0.0, float(self.width - dist) / float(self.width))
        signal = self.bias + frac * 2 * self.amplitude
        noise = self.noise * self.amplitude * random.gauss(0.0, 1.0)
        return signal + noise

if __name__ == "__main__":
    print "This is a module for defining test-signal generators."
