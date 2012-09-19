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
import main as l

class LPSVD_Acceptance_Tests(unittest.TestCase):
    def setUp(self):
       fun = lambda c: abs(abs(c) - 1.0) <= 0.015
        
       self.specs = specs = [(5.0, 0.0, 1.0/45.0, 3.0),
                             (10.0, 0.0, 1.0/20.0, 12.0)]
       self.series = data = s.Periodic(specs, noise=0.0).time_series(100)
       self.case = l.LPSVD(data, count=4.0, filterf=fun)
    
    def test_LPSVD(self):
        decomp = self.case.decomposition()
        self.assertEqual(len(self.specs), decomp.count())
        for pair in zip(self.specs, decomp.summary()):
            for exp,comp in zip(pair[0], pair[1]):
                self.assertTrue(abs(exp - comp) <= 0.001)
    
class LPSVD_LinearFitSpec(unittest.TestCase):
    def setUp(self):
        pass
    def tearDown(self):
        pass

class LPSVD_LinearAlgebraSpec(unittest.TestCase):
    def setUp(self):
        pass
    def tearDown(self):
        pass    

class MockCounter:
    def count_signals(self, series):
        return "Waffle Iron"

class LPSVD_CountingSpec(unittest.TestCase):
    def setUp(self):
        self.case = l.LPSVD(None)
    
    def test_fixed_signal_count(self):
        n = random.randint(1,100)
        self.case.count = n
        self.case.counter = None
        
        count = self.case.get_signal_count([])
        self.assertEqual(count, n)
    
    def test_outsourced_signal_count(self):
        self.case.count = None
        self.case.counter = MockCounter()
        
        count = self.case.get_signal_count([])
        self.assertEqual(count, "Waffle Iron")
    
    def test_internal_signal_count(self):
        self.case.count = None
        self.case.counter = None
        
        n = random.randint(1,100)
        count = self.case.get_signal_count(range(n))
        self.assertTrue(count >= 0)
        self.assertTrue(count <= n)
    
    def test_bias_filter(self):
        data = range(10)
        n = random.randint(1,9)
        signals = data[:n]
        noise = data[n:]
        bias = float(sum(noise)) / float(len(noise))
        
        expected = [s - bias for s in signals]
        filtered = self.case.bias_filter(data, n).tolist()
        
        for e,c in zip(expected, filtered):
            self.assertTrue(abs(e-c) <= 0.001)
    
    def tearDown(self):
        pass

class LPSVD_SetupSpec(unittest.TestCase):
    def setUp(self):
        self.case = l.LPSVD(range(10))
    
    def test_predictions_vecto(self):
        avector = self.case.predictions_vector()
        self.assertEqual(avector.tolist(), [0,1,2])
    
    def test_prediction_matrix(self):
        amatrix = self.case.prediction_matrix()
        self.assertEqual(amatrix[:,0].tolist(), [1,2,3])
        self.assertEqual(amatrix[0,:].tolist(), [i+1 for i in range(7)])
    
    def tearDown(self):
        pass

if __name__ == "__main__":
    unittest.main()
