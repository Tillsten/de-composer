#!/usr/bin/epython

import sys
import os.path

p = os.path.realpath(__file__)
q = os.path.split(os.path.dirname(p))
sys.path.append(os.path.join(q[0], "src"))
del p, q # keep globals clean

import unittest
import random
from math import pi
import decomposition as d

class DecompositionSpec(unittest.TestCase):
    def setUp(self):
        self.t_n = n = random.randint(1,15)
        self.t_amps = [20.0 * random.random() for i in range(n)]
        self.t_decays = [2.0 * random.random() for i in range(n)]
        self.t_freqs = [1.0/random.uniform(5.0,100.0) for i in range(n)]
        self.t_phases = [2*pi * (random.random() - 0.5) for i in range(n)]
        
        self.t_bias = 5.0 * random.random()
        self.specs = specs = zip(self.t_amps,
                                 self.t_decays,
                                 self.t_freqs,
                                 self.t_phases)
        self.case = d.Decomposition(specs, self.t_bias)
    
    def test_initialization(self):
        self.assertTrue(isinstance(self.case, d.Decomposition))
    
    def _test_attribute_fidelity(self, alist, blist):
        self.assertEqual(len(alist), len(blist))
        for a,b in zip(alist, blist):
            self.assertEqual(a, b)
    
    def test_frequencies(self):
        self._test_attribute_fidelity(self.t_freqs, self.case.freqs)
    
    def test_amplitudes(self):
        self._test_attribute_fidelity(self.t_amps, self.case.amps)
    
    def test_decays(self):
        self._test_attribute_fidelity(self.t_decays, self.case.decays)
    
    def test_periods(self):
        periods = [1.0/f for f in self.t_freqs]
        self._test_attribute_fidelity(periods, self.case.periods)
    
    def test_phases(self):
        self._test_attribute_fidelity(self.t_phases, self.case.phases)
    
    def test_time_series(self):
        length = random.randint(10,150)
        series = self.case.time_series(length)
        self.assertEqual(len(series), length)
        for v in series:
            self.assertTrue(v <= sum(self.t_amps) + self.t_bias)
            self.assertTrue(v >= -1*sum(self.t_amps) + self.t_bias)

    def test_min_period_limit_time_series(self):
        length = random.randint(100,750)
        limiter = random.choice(self.specs)
        min_per = 1.0 / limiter[2]
        
        series = self.case.period_limit_time_series(length, min_per)
        filtered = filter(lambda s: 1./s[2] >= min_per, self.specs)
        famps = [s[0] for s in filtered]
        
        self.assertEqual(len(series), length)
        for v in series:
            self.assertTrue(v <= sum(famps) + self.t_bias)
            self.assertTrue(v >= -1*sum(famps) + self.t_bias)
    
    def test_max_period_limit_time_series(self):
        length = random.randint(100,750)
        limiter = random.choice(self.specs)
        max_per = 1.0 / limiter[2]
        
        series = self.case.period_limit_time_series(length, max_per, True)
        filtered = filter(lambda s: 1./s[2] <= max_per, self.specs)
        famps = [s[0] for s in filtered]
        
        self.assertEqual(len(series), length)
        for v in series:
            self.assertTrue(v <= sum(famps) + self.t_bias)
            self.assertTrue(v >= -1*sum(famps) + self.t_bias)
    
    def test_filtered_time_series(self):
        length = random.randint(10,150)
        n = random.randint(1,self.t_n)
        
        min_series = self.case.filtered_time_series(length, n)
        mins = sorted(self.specs, key=lambda s: 1.0/s[2])[:n]
        min_amps = [s[0] for s in mins]
        
        self.assertEqual(len(min_series), length)
        for v in min_series:
            self.assertTrue(v <= sum(min_amps) + self.t_bias)
            self.assertTrue(v >= -1*sum(min_amps) + self.t_bias)
    
    def test_reverse_filtered_time_series(self):
        length = random.randint(10,150)
        n = random.randint(1,self.t_n)
        
        max_series = self.case.filtered_time_series(length, n, True)
        maxs = sorted(self.specs, key=lambda s: 1.0/s[2], reverse=True)[:n]
        max_amps = [s[0] for s in maxs]
        
        self.assertEqual(len(max_series), length)
        for v in max_series:
            self.assertTrue(v <= sum(max_amps) + self.t_bias)
            self.assertTrue(v >= -1*sum(max_amps) + self.t_bias)
    
    def test_count(self):
        self.assertEqual(self.t_n, self.case.count())
    
    def test_summary(self):
        summary = self.case.summary()
        self.assertEqual(self.t_n, len(summary))
        for t in summary:
            self.assertTrue(isinstance(t, tuple))
    
    def tearDown(self):
        pass

if __name__ == "__main__":
    unittest.main()
