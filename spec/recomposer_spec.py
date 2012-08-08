#!/usr/bin/epython

import sys
import os.path

p = os.path.realpath(__file__)
q = os.path.split(os.path.dirname(p))
sys.path.append(os.path.join(q[0], "src"))
del p, q # keep globals clean

import unittest
import component as c
import recomposer as r
import random

class MultipleSpec(unittest.TestCase):
    def setUp(self):
        self.test_amp = 10.0
        self.test_comps = [
            c.Component(1.0, 0.0, 1.0/40.0),
            c.Component(2.0, 0.0, 1.0/20.0),
            c.Component(3.0, 0.0, 1.0/10.0),
            c.Component(4.0, 0.0, 1.0/5.0),
            ]
        
        self.test_bias = (random.random() - 0.5) * 20.0
        self.case = r.Recomposer(self.test_comps, self.test_bias)
    
    def test_time_series(self):
        n = random.randint(10,1000)
        series = self.case.time_series(n)
        
        self.assertTrue(len(series) == n)
        
        for v in series:
            self.assertTrue(abs(v - self.test_bias) <= self.test_amp)
    
    def tearDown(self):
        pass

class SingletonSpec(unittest.TestCase):
    def setUp(self):
        self.test_amp = 15.0
        self.test_comp = c.Component(self.test_amp, 0.0, 0.10, offset=0.0)
        self.test_bias = (random.random() - 0.5) * 20.0
        self.case = r.Recomposer([self.test_comp], self.test_bias)
    
    def test_time_series(self):
        n = random.randint(10,1000)
        series = self.case.time_series(n)
        
        self.assertTrue(len(series) == n)
        
        for v in series:
            self.assertTrue(abs(v - self.test_bias) <= self.test_amp)
    
    def tearDown(self):
        pass

if __name__ == "__main__":
    unittest.main()
