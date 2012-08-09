#!/usr/bin/epython

import sys
import os.path

p = os.path.realpath(__file__)
q = os.path.split(os.path.dirname(p))
sys.path.append(os.path.join(q[0], "src"))
del p, q # keep globals clean

import unittest
import random
import signallers as s

class PeriodicSpec(unittest.TestCase):
    def setUp(self):
        pass
    
    def tearDown(self):
        pass

class GaussianSpec(unittest.TestCase):
    def setUp(self):
        self.mean = mu = 20.0 * random.random()
        self.stdev = delta = 5.0 * random.random()
        self.case = s.Gaussian(mu, delta)
    
    def test_initialization(self):
        self.assertTrue(isinstance(self.case, s.Gaussian))
        self.assertEqual(self.case.mean, self.mean)
        self.assertEqual(self.case.stdev, self.stdev)
    
    def test_time_series(self):
        n = random.randint(1,500)
        series = self.case.time_series(n)
        self.assertEqual(len(series), n)
        for v in series:
            self.assertTrue(v <= self.mean + 4*self.stdev)
            self.assertTrue(v >= self.mean - 4*self.stdev)
    
    def tearDown(self):
        pass

class ImpulseSpec(unittest.TestCase):
    def setUp(self):
        self.amplitude = amp = 40.0 * random.random()
        self.width = width = random.randint(1,5)
        self.period = per = random.randint(20, 100)
        self.bias = bias = 5.0 * random.random()
        self.noise = nsr = random.random()
        
        self.case = s.Impulse(amp, width, per, bias, nsr)
    
    def test_initialization(self):
        self.assertTrue(isinstance(self.case, s.Impulse))
        self.assertEqual(self.amplitude, self.case.amplitude)
        self.assertEqual(self.width, self.case.width)
        self.assertEqual(self.period, self.case.period)
        self.assertEqual(self.bias, self.case.bias)
        self.assertEqual(self.noise, self.case.noise)
    
    def test_time_series(self):
        n = random.randint(100,750)
        series = self.case.time_series(n)
        
        min = self.bias - 4*self.noise*self.amplitude
        max = self.bias + 4*self.noise*self.amplitude + self.amplitude
        
        self.assertEqual(n, len(series))
        for v in series:
            self.assertTrue(v <= max)
            self.assertTrue(v >= min)
    
    def tearDown(self):
        pass

class StepSpec(unittest.TestCase):
    def setUp(self):
        self.amplitude = amp = 20.0 * random.random()
        self.noise = nsr = random.random()
        self.period = per = random.randint(10,500)
        self.offset = off = random.randint(0, per)
        self.bias = bias = 10.0 * random.random()
        
        self.case = s.Step(amp, per, off, bias, nsr)
    
    def test_initialization(self):
        self.assertTrue(isinstance(self.case, s.Step))
        self.assertEqual(self.case.amplitude, self.amplitude)
        self.assertEqual(self.case.noise, self.noise)
        self.assertEqual(self.case.period, self.period)
        self.assertEqual(self.case.offset, self.offset)
        self.assertEqual(self.case.bias, self.bias)
    
    def test_time_series(self):
        n = random.randint(100,750)
        
        self.case.noise = 0.0
        series = self.case.time_series(n)
        
        self.assertEqual(len(series), n)
        high = self.bias + self.amplitude
        low = self.bias - self.amplitude
        for v in series:
            self.assertTrue(v == high or v == low)
    
    def tearDown(self):
        pass

if __name__ == "__main__":
    unittest.main()
