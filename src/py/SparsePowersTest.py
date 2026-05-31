#!/usr/bin/env python3

# This software is Copyright (C) 2004-2008  Bristol University
# and is released under the GNU General Public License version 2.

import unittest
from TuplePowers import TuplePowers
from SparsePowers import *

from random import Random
gen = Random(6543210)

class Default(unittest.TestCase):

    """Test the properties of the default constructor."""

    def test_call(self):
        m = SparsePowers()
        self.assertRaises(TypeError, m.__call__, 1.0)

    def test_degree(self):
        m = SparsePowers()
        self.assertEqual(m.degree(), 0)

    def test_repr(self):
        m = SparsePowers()
        self.assertEqual(repr(m), 'SparsePowers(1, {})')

    def test_diff_coeff(self):
        m = SparsePowers()
        c, d = m.diff(0)
        self.assertEqual(c, 0)

    def test_diff_pow_coeff(self):
        m = SparsePowers()
        for i in range(10):
            c, d = m.diff_pow(0, i)
            if i == 0:
                self.assertEqual(c, 1)
            else:
                self.assertEqual(c, 0)

    def test_diff_powers(self):
        m = SparsePowers()
        c, d = m.diff(0)
        self.assertEqual(repr(d), 'SparsePowers(1, {})')

    def test_diff_pow_powers(self):
        m = SparsePowers()
        for i in range(10):
            c, d = m.diff_pow(0, i)
            self.assertEqual(repr(d), 'SparsePowers(1, {})')

    def test_pows(self):
        p = SparsePowers((1,))
        for i in range(10):
            self.assertEqual(p**i, SparsePowers((i,)))

def rand_int(max_val):
    return gen.randrange(0, max_val)
    
def rand_int_tuple(length, max_val):
    return tuple([rand_int(max_val) for i in range(length)])
        
class PowersLike(unittest.TestCase):

    def test_empty(self):
        t = ()
        m = TuplePowers(t)
        p = SparsePowers(t)
        self.assertTrue(t == p)
        self.assertTrue(m == p)

    def test_not_eq(self):
        t = ()
        p = SparsePowers(t)
        self.assertTrue(not (TuplePowers((1,)) == p))

    def test_example(self):
        t = (1, 2, 3)
        m = TuplePowers(t)
        p = SparsePowers(t)
        self.assertTrue(t == p)
        self.assertTrue(m == p)

    def test_dict(self):
        t = (1, 2, 3)
        p = SparsePowers(t)
        d = {}
        d[p] = -99.0
        self.assertTrue(p in d)
        self.assertTrue(d[p] == -99.0)

class TupleLike(unittest.TestCase):

    def test_empty(self):
        t = ()
        p = SparsePowers(t)
        self.assertTrue(t == p)

    def test_not_eq(self):
        t = ()
        p = SparsePowers(t)
        self.assertTrue(not ((1,) == p))

    def test_example(self):
        t = (1, 2, 3)
        p = SparsePowers(t)
        self.assertTrue(t == p)

    def test_to_tuple(self):
        for i in range(50):
            t = rand_int_tuple(40, 14)
            m = SparsePowers(t)
            tt = m.to_tuple()
            self.assertTrue(type(tt) == tuple)
            self.assertTrue(t == tt)

class Examples(unittest.TestCase):

    """Test many of the routines for a set of examples."""

    def setUp(self):
        examples = [(),
                    (1,),
                    (2,),
                    (1,2,3),
                    (1,1,0,5)]
        for bits in range(5,10):
            max_val = (1<<bits)-1
            for length in range(1,10):
                for case in range(10):
                    t = rand_int_tuple(length, max_val)
                    examples.append(t)
        self.examples = examples

    def _tuple_to_nonzero_dict(self, t):
        d = {}
        for i, e in enumerate(t):
            if e != 0:
                d[i] = e
        return d

    def test_both_constructors(self):
        for eg in self.examples:
            d = self._tuple_to_nonzero_dict(eg)
            p0 = SparsePowers(eg)
            p1 = SparsePowers(len(eg), d)
            self.assertEqual(p0, p1)

    def test_call_wrong_len(self):
        for eg in self.examples:
            p = SparsePowers(eg)
            for l in range(0, len(eg)*2):
                x = rand_int_tuple(l, 10)
                if not l==len(eg):
                    self.assertRaises(IndexError, p.__call__, x)

    def test_call_non_seq(self):
        for eg in self.examples:
            p = SparsePowers(eg)
            self.assertRaises(TypeError, p.__call__, 1.0)

    def test_call_all_zero(self):
        for eg in self.examples:
            p = SparsePowers(eg)
            zero = (0.0,)*len(eg)
            if p.degree()==0:
                self.assertEqual(p(zero), 1.0)
            else:
                self.assertEqual(p(zero), 0.0)

    def test_call_all_one(self):
        """any monomial (no coeff) evaluated at (1.0,)*len gives 1.0"""
        for eg in self.examples:
            p = SparsePowers(eg)
            one = (1.0,)*len(eg)
            self.assertEqual(p(one), 1.0)

    def test_call_any_zero(self):
        """any monomial (no coeff) evaluated at (1.0,)*len gives 1.0"""
        for eg in self.examples:
            p = SparsePowers(eg)
            for var in range(len(eg)):
                x = [float(i+1) for i in rand_int_tuple(len(eg), 3)]
                x[var] = 0.0
                if p[var]==0:
                    self.assertTrue(not p(x)==0.0)
                else:
                    self.assertEqual(p(x), 0.0)

    def test_call_negative_counts(self):
        for eg in self.examples:
            p = SparsePowers(eg)
            deg = sum(eg)
            neg = sum([1 for i in eg if i%2])%2
            eno = (-1.0,)*len(eg)
            r = p(eno)
            if deg==0:
                self.assertTrue(r==1.0)
            if neg:
                self.assertTrue(r==-1.0)
            else:
                self.assertTrue(r==1.0)

    def test_number_of_variables(self):
        for eg in self.examples:
            p = SparsePowers(eg)
            self.assertEqual(p.number_of_variables(), len(eg))

    def test_degree(self):
        for eg in self.examples:
            p = SparsePowers(eg)
            self.assertEqual(p.degree(), sum(eg))

    def test_repr(self):
        for eg in self.examples:
            p = SparsePowers(eg)
            d = {}
            for i, po in enumerate(eg):
                if po > 0:
                    d[i] = po
            self.assertEqual(repr(p), 'SparsePowers(%d, %s)'%(len(eg), d))

    def test_pow_zero_is_one(self):
        for eg in self.examples:
            p = SparsePowers(eg)
            self.assertEqual(p**0, SparsePowers((0,)*len(eg)))

    def test_pow_one_is_same(self):
        for eg in self.examples:
            p = SparsePowers(eg)
            self.assertEqual(p**1, p)

    def test_pow(self):
        for eg in self.examples:
            p = SparsePowers(eg)
            for i in range(10):
                eg10 = tuple([i*j for j in eg])
                self.assertEqual(p**i, SparsePowers(eg10))

    def test_mul(self):
        lengths = 50
        cases = 20
        bits = 25
        max_val = int((1<<bits)-1)/2
        for length in range(lengths):
            for case in range(cases):
                pt = rand_int_tuple(length, max_val)
                p = SparsePowers(pt)
                qt = rand_int_tuple(length, max_val)
                q = SparsePowers(qt)
                rt = tuple([a+b for a,b in zip(pt, qt)])
                r = SparsePowers(rt)
                self.assertEqual(p*q, r)
                z = SparsePowers((0,)*length)
                self.assertEqual(p*z, p)
                self.assertEqual(q*z, q)
                self.assertEqual(z*p, p)
                self.assertEqual(z*q, q)
                d = {}
                for i, po in enumerate(rt):
                    if po > 0:
                        d[i] = po
                self.assertEqual(repr(p*q),
                                  'SparsePowers(%d, %s)'%(length,
                                                          repr(d)))

    def test_equal_self(self):
        for eg in self.examples:
            p = SparsePowers(eg)
            self.assertEqual(p, p)

    def test_less_equal_self(self):
        for eg in self.examples:
            p = SparsePowers(eg)
            self.assertTrue(p<=p)

    def test_greater_equal_self(self):
        for eg in self.examples:
            p = SparsePowers(eg)
            self.assertTrue(p>=p)

    def test_not_greater_self(self):
        for eg in self.examples:
            p = SparsePowers(eg)
            self.assertTrue(not (p>p))

    def test_not_less_self(self):
        for eg in self.examples:
            p = SparsePowers(eg)
            self.assertTrue(not (p<p))

    def test_not_not_equal_self(self):
        for eg in self.examples:
            p = SparsePowers(eg)
            self.assertTrue(not (p!=p))

    def test_equal_other_same(self):
        for eg in self.examples:
            p = SparsePowers(eg)
            self.assertEqual(p, SparsePowers(eg))

    def test_diff(self):
        for eg in self.examples:
            p = SparsePowers(eg)
            for var in range(len(eg)):
                coeff, q = p.diff(var)
                self.assertEqual(coeff, eg[var])
                msg = ('d(%d)[%s]'%(var, repr(eg)))+' -> '+repr(q)
                for j in range(len(eg)):
                    if j==var:
                        if eg[j]==0:
                            self.assertEqual(coeff, 0.0, msg)
                        else:
                            self.assertEqual(q[j], eg[j]-1, msg)
                            self.assertEqual(coeff, eg[j], msg)
                    else:
                        if eg[var] != 0:
                            self.assertEqual(q[j], eg[j], msg)

    def test_diff_pow0(self):
        for eg in self.examples:
            p = SparsePowers(eg)
            for var in range(len(eg)):
                coeff0, q0 = p.diff_pow(var, 0)
                self.assertEqual(coeff0, 1.0)
                self.assertEqual(q0, p)

    def test_diff_pow1(self):
        for eg in self.examples:
            p = SparsePowers(eg)
            for var in range(len(eg)):
                coeff, q = p.diff(var)
                coeff1, q1 = p.diff_pow(var, 1)
                self.assertEqual(coeff1, coeff)
                self.assertEqual(q1, q)

    def test_diff_pow(self):
        for eg in self.examples:
            p = SparsePowers(eg)
            for var in range(len(eg)):
                coeff0, q0 = p.diff_pow(var, 0)
                self.assertEqual(coeff0, 1.0)
                self.assertEqual(q0, p)
                coeff, q = p.diff(var)
                coeff1, q1 = p.diff_pow(var, 1)
                self.assertEqual(coeff1, coeff)
                self.assertEqual(q1, q)
                for pow in range(5):
                    coeff, q = p.diff_pow(var, pow)
                    cop = p.copy()
                    c = 1.0
                    for i in range(pow):
                        co, cop = cop.diff(var)
                        c *= co
                    self.assertEqual(cop, q)
                    err = abs(coeff - c)
                    self.assertTrue(err < 1.0e-12, err)

class Diff(unittest.TestCase):

    """Diff-specific range tests."""

    def test_negative_index(self):
        for i in range(-10, 0):
            m = SparsePowers()
            self.assertRaises(IndexError, m.diff, i)

    def test_bad_index(self):
        for i in range(1, 10):
            m = SparsePowers()
            self.assertRaises(IndexError, m.diff, i)

class Pow(unittest.TestCase):

    """Pow-specific range tests."""

    def test_negative_pow(self):
        for i in range(-10, 0):
            m = SparsePowers()
            self.assertRaises(ValueError, m.__pow__, i)

def suite():
    suites = []
    suites.append(unittest.makeSuite(PowersLike))
    suites.append(unittest.makeSuite(TupleLike))
    suites.append(unittest.makeSuite(Default))
    suites.append(unittest.makeSuite(Examples))
    suites.append(unittest.makeSuite(Diff))
    suites.append(unittest.makeSuite(Pow))
    return unittest.TestSuite(suites)

if __name__ == "__main__":
    unittest.main(defaultTest='suite')
