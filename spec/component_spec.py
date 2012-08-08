#!/usr/bin/epython

import sys
import os.path

p = os.path.realpath(__file__)
q = os.path.split(os.path.dirname(p))
sys.path.append(os.path.join(q[0], "src"))
del p, q # keep globals clean

import component as c
import unittest
import random
from math import pi,e

class ComponentSpec(unittest.TestCase):
    def setUp(self):
        self.test_amp = random.random() * 10.0
        self.test_decay = 2.0 * (random.random() - 0.5)
        self.test_freq = random.uniform(0.0001, 0.02)
        self.test_phase = (random.random() - 0.5) * 2.0 * pi
        self.test_offset = random.random() * (1.0 / self.test_freq)
        self.pcase = c.Component(self.test_amp,
                                 self.test_decay,
                                 self.test_freq,
                                 phase=self.test_phase)
        self.ocase = c.Component(self.test_amp,
                                 self.test_decay,
                                 self.test_freq,
                                 offset=self.test_offset)
    
    def test_initialization(self):
        for case in [self.pcase, self.ocase]:
            self.assertEqual(self.test_amp, case.amp)
            self.assertEqual(self.test_decay, case.decay)
            self.assertEqual(self.test_freq, case.freq)
            self.assertEqual(1.0/self.test_freq, case.period)
        self.assertEqual(self.test_phase, self.pcase.phase)
        self.assertEqual(self.test_offset, self.ocase.offset)
    
    def test_conversion_to_offset(self):
        case = self.pcase
        self.assertTrue(case.offset >= 0)
        self.assertTrue(case.offset <= (1.0/self.test_freq))
    
    def test_conversion_to_phase(self):
        case = self.ocase
        self.assertTrue(case.phase >= -1*pi)
        self.assertTrue(case.phase <= pi)
    
    def test_o_tuple(self):
        t = self.ocase.to_tuple()
        self.assertEqual(self.test_amp, t[0])
        self.assertEqual(self.test_decay, t[1])
        self.assertEqual(self.test_freq, t[2])
        self.assertEqual(self.test_offset, t[3])
    
    def test_p_tuple(self):
        t = self.pcase.to_tuple(True)
        self.assertEqual(self.test_amp, t[0])
        self.assertEqual(self.test_decay, t[1])
        self.assertEqual(self.test_freq, t[2])
        self.assertEqual(self.test_phase, t[3])
    
    def test_value(self):
        for t in range(100):
            m = e ** (-1 * self.test_decay*t)
            self.assertTrue(abs(self.pcase.value(t)) <= m*self.test_amp)
            self.assertTrue(abs(self.ocase.value(t)) <= m*self.test_amp)
    
    def tearDown(self):
        pass

if __name__ == "__main__":
    unittest.main()
