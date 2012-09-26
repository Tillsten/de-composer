#!/usr/bin/epython

import sys
import os.path

p = os.path.realpath(__file__)
q = os.path.split(os.path.dirname(p))
sys.path.append(os.path.join(q[0], "src"))
del p, q # keep globals clean

import unittest
import random
import numpy as np
import statistics as s

class JTK_Class_Spec(unittest.TestCase):
    """Describe JTK Cycle class:"""
    
    def setUp(self):
        self.test_n = n = random.randint(10,1000)
        self.series = series = np.random.rand(n)
        
        self.case = s.JTK(series)
    
    def test_initialization(self):
        """It should properly initialize an instance of JTK."""
        self.assertTrue(isinstance(self.case, s.JTK))
    
    def test_memoization(self):
        """It should correctly initialize with the values provided."""
        self.assertTrue(np.all(np.equal(self.series, self.case.series)))
        self.assertEqual(self.case.N, self.test_n)
    
    def test_npcast(self):
        """It should upcast the initialization series to numpy array."""
        self.assertTrue(isinstance(self.case.series, np.ndarray))
    
    def tearDown(self):
        pass

class JTK_Function_Spec(unittest.TestCase):
    """Describe JTK Class functionality:"""
    
    def setUp(self):
        N = random.randint(10,1000)
        
        self.negative_case = s.JTK(self._negative_series(N))
        
        self.test_per = per = random.randint(N/4,3*N/4)
        self.test_off = offset = random.randint(0,per)
        self.positive_case = s.JTK(self._positive_series(N,per,offset))
    
    def _negative_series(self, N):
        series = np.ones(N) + (0.25 * np.random.randn(N))
        return series
    
    def _positive_series(self, N, period, offset):
        pihat = np.round(np.pi,4)
        factor = 2 * pihat / period
        
        times = np.arange(N) * factor
        times = times + (offset * factor)
        
        series = np.cos(times)
        return series
    
    def test_positive(self):
        """It should correctly identify the positive controls."""
        per = self.test_per
        off = self.test_off
        
        s_val, p_val = self.positive_case.run_series(per, off)
        self.assertTrue(p_val < 0.01)
    
    def test_negative(self):
        """It should correctly decline the negative controls."""
        per = self.test_per
        off = self.test_off
        
        s_val, p_val = self.negative_case.run_series(per, off)
        self.assertTrue(p_val > 0.01)
        
        per = random.randint(1,self.negative_case.N)
        p_val = self.negative_case.run_series(per, 0.0)[1]
        self.assertTrue(p_val > 0.01)
    
    def test_relative_period(self):
        """It should score correctly based on relative period fit."""
        per = self.test_per
        under = per / 2
        over = per * 2
        off = self.test_off
        
        p_on = self.positive_case.run_series(per, off)[1]
        p_under = self.positive_case.run_series(per, under)[1]
        p_over = self.positive_case.run_series(per, over)[1]
        
        self.assertTrue(p_on < p_under)
        self.assertTrue(p_on < p_over)
    
    def test_relative_offset(self):
        """It should score correctly based on relative offset fit."""
        per = self.test_per
        off = self.test_off
        shorter = random.randint(0,off)
        longer = random.randint(off+1,per)
        
        p_on = self.positive_case.run_series(per,off)[1]
        p_shorter = self.positive_case.run_series(per,shorter)[1]
        p_longer = self.positive_case.run_series(per,longer)[1]
        
        self.assertTrue(p_on <= p_shorter)
        self.assertTrue(p_on <= p_longer)
    
    def tearDown(self):
        pass

class JTK_Score_Spec(unittest.TestCase):
    """Describe JTK score generation:"""
    
    def setUp(self):
        self.case = s.JTK(np.ones(1))
    
    def test_score_trivial_a(self):
        """It should generate a zero score for flatline reference."""
        data = np.arange(12)
        ref = np.ones(12)
        expect = 0.0
        actual = self.case.s_score(data,ref)
        self.assertEqual(expect, actual)

    def test_score_trivial_b(self):
        """It should generate a zero score for flatline test series."""
        data = np.ones(12)
        ref = np.arange(12)
        expect = 0.0
        actual = self.case.s_score(data,ref)
        self.assertEqual(expect, actual)
    
    def test_score_a(self):
        """It should generate a correct score for test series A."""
        data = np.array([1,3,2,4],dtype='float')
        ref = np.arange(4)
        expect = 4.0
        actual = self.case.s_score(data,ref)
        self.assertEqual(expect, actual)
    
    def test_score_b(self):
        """It should generate a correct score for test series B."""
        data = np.array([4,3,2,1],dtype='float')
        ref = np.arange(4)
        expect = -6.0
        actual = self.case.s_score(data,ref)
        self.assertEqual(expect, actual)
    
    def test_score_c(self):
        """It should generate a correct score for test series C."""
        data = np.array([1,2,4,3],dtype='float')
        ref = np.array([3,2,1,4],dtype='float')
        expect = -2.0
        actual = self.case.s_score(data,ref)
        self.assertEqual(expect, actual)
    
    def tearDown(self):
        pass

if __name__ == "__main__":
    unittest.main()
