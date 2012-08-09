#!/usr/bin/epython

import sys
import os.path
sys.path.append(os.path.dirname(os.path.realpath(__file__)))

import component as c
import recomposer as r

class Decomposition():
    """The Decomposition class is the result of a decomposition procedure.
       Instances can summarize the decomposition as well as reconstitute
       data series based on their components."""
    
    def __init__(self, specs, bias=0.0):
        """Initializes a decomposition object."""
        self._bias = bias
        self._components = []
        for spec in specs:
            # For historical reasons, given as: (amp, decay, freq, phase)
            amp, decay, freq, ph = spec
            self._components.append(c.Component(amp, decay, freq, phase=ph))
    
    def get_frequencies(self):
        return [c.freq for c in self._components]
    
    def get_amplitudes(self):
        return [c.amp for c in self._components]
    
    def get_decays(self):
        return [c.decay for c in self._components]
    
    def get_periods(self):
        return [c.period for c in self._components]
    
    def get_phases(self):
        return [c.phase for c in self._components]
    
    def get_offsets(self):
        return [c.phase for c in self._components]
    
    def time_series(self, length):
        """Builds a recomposed time series based on all components."""
        maker = r.Recomposer(self._components, self._bias)
        return maker.time_series(length)
    
    def filtered_time_series(self, length, n, should_reverse=False):
        """Generates a time series based on a subset of components,
           specified by a slice tuple. Assumed to be period sorted..."""
        sorts = self._components[:]
        sorts.sort(key=lambda c: c.period, reverse=should_reverse)
        if isinstance(n, tuple) and len(n) == 2:
            filtered = sorts[n[0]:n[1]]
        elif isinstance(n, int):
            filtered = sorts[:n]
        else:
            raise Exception("Please argue n as integer or slice tuple!")
        maker = r.Recomposer(filtered, self._bias)
        return maker.time_series(length)
    
    def count_components(self):
        """Returns the number of components in the decomposition"""
        return len(self._components)
    
    def make_summary(self):
        """Returns a concise summary of decomposition components."""
        return [c.to_tuple() for c in self._components]
        
if __name__ == "__main__":
    print "This module defines a class for component-wise Decompositions."
