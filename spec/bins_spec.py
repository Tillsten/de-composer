#!/usr/bin/epython

import sys
import os.path

p = os.path.realpath(__file__)
q = os.path.split(os.path.dirname(p))
sys.path.append(os.path.join(q[0], "src"))
del p, q # keep globals clean

import unittest
import bins as b
import random

class SBinSpec(unittest.TestCase):
    def setUp(self):
        pass
    
    def test_singletons(self):
        series = range(11)
        binned = b.sbin(series, 1)
        self.assertEqual(binned, series)
    
    def test_doubles(self):
        series = range(11)
        binned = b.sbin(series, 2)
        self.assertEqual(len(binned), 10)
        expect = map(sum, zip(range(10),range(1,11)))
        self.assertEqual(expect, binned)
    
    def test_quads(self):
        series = [2*i for i in range(7)]
        binned = b.sbin(series, 4)
        self.assertEqual([12, 20, 28, 36], binned)
    
    def tearDown(self):
        pass

class ABinSpec(unittest.TestCase):
    def setUp(self):
        pass
    
    def test_singletons(self):
        series = [random.random() for i in range(10)]
        binned = b.abin(series, 1)
        self.assertEqual(binned, series)
    
    def test_doubles(self):
        series = range(6)
        series.reverse()
        binned = b.abin(series, 2)
        self.assertEqual(binned, [4.5, 3.5, 2.5, 1.5, 0.5])
    
    def test_quads(self):
        series = [3*i for i in range(7)]
        binned = b.abin(series, 4)
        self.assertEqual(binned, [4.5, 7.5, 10.5, 13.5])
    
    def tearDown(self):
        pass

if __name__ == "__main__":
    unittest.main()
