#!/usr/bin/epython

import sys
import os.path

p = os.path.realpath(__file__)
q = os.path.split(os.path.dirname(p))
sys.path.append(os.path.join(q[0], "src"))
del p, q # keep globals clean

import unittest
import random
from math import ceil
import counters as c

class RelativeMassCounterSpec(unittest.TestCase):
    def setUp(self):
        self.counter = c.RelativeMassCounter(0.5)
    
    def test_count_signals(self):
        n = random.randint(4,100)
        test_series = range(n)
        
        self.counter.fraction = 0.25
        expected = 3 * n / 4
        if expected % 2 == 1:
            expected += 1
        self.assertEqual(self.counter.count_signals(test_series), expected)
        
        self.counter.fraction = 0.5
        expected = n / 2
        if expected % 2 == 1:
            expected += 1
        self.assertEqual(self.counter.count_signals(test_series), expected)
        
        random.shuffle(test_series)
        self.assertEqual(self.counter.count_signals(test_series), expected)
        
    def tearDown(self):
        pass

class MassFractionCounterSpec(unittest.TestCase):
    def setUp(self):
        self.fraction = frac = random.random()
        self.case = c.MassFractionCounter(frac)
    
    def test_initialization(self):
        self.assertTrue(isinstance(self.case, c.Counter))
    
    def test_count_signals_fixed(self):
        fixies = [1.0 for i in range(100)]
        n_fixies = self.case.count_signals(fixies)
        self.assertTrue(abs(n_fixies - ceil(self.fraction * 100)) <= 1)
        self.assertTrue(n_fixies > 0)
        self.assertTrue(n_fixies % 2 == 0)
    
    def test_count_signals_random(self):
        randos = [10*random.random() for i in range(random.randint(10, 1000))]
        n_randos = self.case.count_signals(randos)
        self.assertTrue(n_randos > 0)
        self.assertTrue(n_randos % 2 == 0)
    
    def tearDown(self):
        pass

if __name__ == "__main__":
    unittest.main()
