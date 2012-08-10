#!/usr/bin/epython

import sys
import os.path

p = os.path.realpath(__file__)
q = os.path.split(os.path.dirname(p))
sys.path.append(os.path.join(q[0], "src"))
del p, q # keep globals clean

import unittest
import random
import utility as u

class SpecMakerSpec(unittest.TestCase):
    
    def test_zeroth_case(self):
        made = u.make_specs(0)
        self.assertEqual([], made)
    
    def test_random_case(self):
        n = random.randint(1,20)
        made = u.make_specs(n)
        self.assertEqual(n, len(made))
        for spec in made:
            self.assertTrue(isinstance(spec, tuple))
            self.assertEqual(len(spec), 4)

class MeanSqErrorSpec(unittest.TestCase):
    
    def test_zero_error(self):
        a = range(10)
        b = a[:]
        err = u.mean_sq_error(a,b)
        self.assertEqual(0, err)
    
    def test_unequal_lengths(self):
        a = range(10)
        b = range(100)
        err = u.mean_sq_error(a,b)
        self.assertEqual(0, err)
    
    def test_errors(self):
        a = [1,1,1]
        b = [1,2,3]
        err = u.mean_sq_error(a,b)
        expected = 5.0/3.0
        self.assertEqual(err, expected)

class DeltasSpec(unittest.TestCase):
    def test_deltas(self):
        a = [1,1,1]
        b = [2,-2,2]
        ds = u.deltas(a,b)
        self.assertEqual(ds, [1,-3,1])

if __name__ == "__main__":
    unittest.main()
