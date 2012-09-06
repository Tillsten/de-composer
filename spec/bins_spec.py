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

class TCBinsSpec(unittest.TestCase):
    def test_uniforms(self):
        priors = [1.0 for i in range(50)]
        posts = b.tcbin(priors, 1.0)
        for p in posts:
            self.assertEqual(p, 1.0)
    
    def test_distribution(self):
        priors = [0.0 for i in range(7)]
        priors[3] = 1.0
        posts = b.tcbin(priors,3.0)
        self.assertEqual(posts[0], 0.0)
        self.assertEqual(posts[6], 0.0)
        for p in posts[2:-1]:
            self.assertTrue(0.0 < p < 0.3)

class TCWidthSpec(unittest.TestCase):
    def test_zero(self):
        self.assertEqual(b.tc_width(0), 0)
    
    def test_computed(self):
        argued = 2.0
        expected = 1.6924
        self.assertTrue(abs(b.tc_width(argued) - expected) <= 0.001)

class GSBinSpec(unittest.TestCase):
    def test_uniforms(self):
        priors = [1.0 for i in range(50)]
        posts = b.gsbin(priors, 1.0)
        for p in posts:
            self.assertEqual(1.0, p)
    
    def test_distribution(self):
        priors = [0.0 for i in range(7)]
        priors[3] = 1.0
        posts = b.gsbin(priors,1.0)
        mn = 0.005
        mx = 0.4
        for p in posts:
            self.assertTrue(mn <= p <= mx)
        self.assertEqual(max(posts), posts[3])


class GSWidthSpec(unittest.TestCase):
    def test_zero(self):
        self.assertEqual(b.gs_width(0), 0)
    
    def test_computed(self):
        argued = 2.0
        expected = 0.8493
        self.assertTrue(abs(b.gs_width(argued) - expected) < 0.01)

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
        exs = [ex * 2.50663 for ex in exs]
        ks = [b.gs_kernel(d, sd) for d in ds]
        for p in zip(ks, exs):
            self.assertTrue(abs(p[0]-p[1])/p[1] <= 0.05)

if __name__ == "__main__":
    unittest.main()
