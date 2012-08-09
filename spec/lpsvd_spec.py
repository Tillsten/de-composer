#!/usr/bin/epython

import sys
import os.path

p = os.path.realpath(__file__)
q = os.path.split(os.path.dirname(p))
sys.path.append(os.path.join(q[0], "src"))
del p, q # keep globals clean

import unittest
from lpsvd import LPSVD

class LPSVD_Acceptance_Tests(unittest.TestCase):
    def setUp(self):
        pass
    
    def tearDown(self):
        pass

class LPSVD_Spec(unittest.TestCase):
    def setUp(self):
        self.case = LPSVD(map(float, range(100)))
    
    def test_polynomial_coefficients(self):
        pass
    
    def test_bias_filter(self):
        pass
    
    def test_get_signal_count(self):
        pass
    
    def test_predictions_vecto(self):
        pass
    
    def test_prediction_matrix(self):
        pass
    
    def tearDown(self):
        pass

if __name__ == "__main__":
    unittest.main()
