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

class TricubicKernelSpec(unittest.TestCase):
    def test_kernel(self):
        w = 3.0
        ds = [-3.0, -2.0, -1.0, 0.0, 1.0, 2.0, 3.0]
        ks = [b.tc_kernel(d,w) for d in ds]
        exs = [(1 - (abs(d)/w)**3)**3 for d in ds]
        for p in zip(ks, exs):
            self.assertEqual(p[0],p[1])

class GaussianKernelSpec(unittest.TestCase):
    def test_kernel(self):
        sd = 1.0
        ds = [-3.0, -2.0, -1.0, 0.0, 1.0, 2.0, 3.0]
        exs = [.0044, .05340, .2419, .3989, .2419, .0540, .0044]
        ks = [b.gs_kernel(d, sd) for d in ds]
        self.assertTrue(abs(sum(ks) - 1.0) <= 0.01)
        for p in zip(ks, exs):
            self.assertTrue(abs(p[0]-p[1])/p[1] <= 0.05)

if __name__ == "__main__":
    unittest.main()
