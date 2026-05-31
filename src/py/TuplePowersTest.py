#!/usr/bin/env python3

# This software is Copyright (C) 2004-2008  Bristol University
# and is released under the GNU General Public License version 2.

import unittest
from TuplePowers import TuplePowers

from random import Random
gen = Random(6543210)

class Default(unittest.TestCase):

    """Test the properties of the default constructor."""

    def test_call(self):
        m = TuplePowers()
        self.assertRaises(TypeError, m.__call__, 1.0)

    def test_degree(self):
        m = TuplePowers()
        self.assertEqual(m.degree(), 0)

    def test_repr(self):
        m = TuplePowers()
        self.assertEqual(repr(m), 'TuplePowers((0,))')

    def test_diff_coeff(self):
        m = TuplePowers()
        c, d = m.diff(0)
        self.assertEqual(c, 0)

    def test_diff_powers(self):
        m = TuplePowers()
        c, d = m.diff(0)
        self.assertEqual(repr(d), 'TuplePowers((0,))')

    def test_pows(self):
        p = TuplePowers((1,))
        for i in range(10):
            self.assertEqual(p**i, TuplePowers((i,)))

def rand_int(max_val):
    return gen.randrange(0, max_val)
    
def rand_int_tuple(length, max_val):
    return tuple([rand_int(max_val) for i in range(length)])

class TupleLike(unittest.TestCase):

    def test_empty(self):
        t = ()
        p = TuplePowers(t)
        self.assertTrue(t == p)

    def test_not_eq(self):
        t = ()
        p = TuplePowers(t)
        self.assertTrue(not ((1,) == p))

    def test_example(self):
        t = (1, 2, 3)
        p = TuplePowers(t)
        self.assertTrue(t == p)

    def test_dict(self):
        t = (1, 2, 3)
        p = TuplePowers(t)
        d = {}
        d[t] = -99.0
        self.assertTrue(p in d)
        self.assertTrue(d[p] == d[t])

    def test_to_tuple(self):
        for i in range(50):
            t = rand_int_tuple(40, 20)
            m = TuplePowers(t)
            tt = m.to_tuple()
            self.assertTrue(type(tt) == tuple)
            self.assertTrue(t == tt)

class Examples(unittest.TestCase):

    """Test many of the routines for a set of examples."""

    def setUp(self):
        self.examples = [(),
                         (1,),
                         (2,),
                         (1,2,3),
                         (1,1,0,5)]
        for max_val in range(5, 500, 50):
            for length in range(1,10):
                for case in range(10):
                    t = rand_int_tuple(length, max_val)
                    self.examples.append(t)

    def _tuple_to_nonzero_dict(self, t):
        d = {}
        for i, e in enumerate(t):
            if e != 0:
                d[i] = e
        return d

    def test_both_constructors(self):
        for eg in self.examples:
            d = self._tuple_to_nonzero_dict(eg)
            p0 = TuplePowers(eg)
            p1 = TuplePowers(len(eg), d)
            self.assertEqual(p0, p1)

    def test_call_wrong_len(self):
        for eg in self.examples:
            p = TuplePowers(eg)
            for l in range(0, len(eg)*2):
                x = rand_int_tuple(l, 10)
                if not l==len(eg):
                    self.assertRaises(IndexError, p.__call__, x)

    def test_call_non_seq(self):
        for eg in self.examples:
            p = TuplePowers(eg)
            self.assertRaises(TypeError, p.__call__, 1.0)

    def test_call_all_zero(self):
        for eg in self.examples:
            p = TuplePowers(eg)
            zero = (0.0,)*len(eg)
            if p.degree()==0:
                self.assertEqual(p(zero), 1.0)
            else:
                self.assertEqual(p(zero), 0.0)

    def test_call_all_one(self):
        """any monomial (no coeff) evaluated at (1.0,)*len gives 1.0"""
        for eg in self.examples:
            p = TuplePowers(eg)
            one = (1.0,)*len(eg)
            self.assertEqual(p(one), 1.0)

    def test_call_any_zero(self):
        """any monomial (no coeff) evaluated at (1.0,)*len gives 1.0"""
        for eg in self.examples:
            p = TuplePowers(eg)
            for var in range(len(eg)):
                x = [float(i+1) for i in rand_int_tuple(len(eg), 3)]
                x[var] = 0.0
                if p[var]==0:
                    self.assertTrue(not p(x)==0.0)
                else:
                    # test for NaN, doubles may/will overflow
                    px = p(x)
                    if px==px:
                        self.assertEqual(px, 0.0)

    def test_call_negative_counts(self):
        for eg in self.examples:
            p = TuplePowers(eg)
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
            p = TuplePowers(eg)
            self.assertEqual(p.number_of_variables(), len(eg))

    def test_degree(self):
        for eg in self.examples:
            p = TuplePowers(eg)
            self.assertEqual(p.degree(), sum(eg))

    def test_repr(self):
        for eg in self.examples:
            p = TuplePowers(eg)
            self.assertEqual(repr(p), 'TuplePowers(%s)'%repr(eg))

    def test_pow_zero_is_one(self):
        for eg in self.examples:
            p = TuplePowers(eg)
            self.assertEqual(p**0, TuplePowers((0,)*len(eg)))

    def test_pow_one_is_same(self):
        for eg in self.examples:
            p = TuplePowers(eg)
            self.assertEqual(p**1, p)

    def test_pow(self):
        for eg in self.examples:
            p = TuplePowers(eg)
            for i in range(10):
                eg10 = tuple([i*j for j in eg])
                self.assertEqual(p**i, TuplePowers(eg10))

    def test_mul(self):
        lengths = 50
        cases = 20
        max_val = 500
        for length in range(lengths):
            for case in range(cases):
                pt = rand_int_tuple(length, max_val)
                p = TuplePowers(pt)
                qt = rand_int_tuple(length, max_val)
                q = TuplePowers(qt)
                rt = tuple([a+b for a,b in zip(pt, qt)])
                r = TuplePowers(rt)
                self.assertEqual(p*q, r)
                z = TuplePowers((0,)*length)
                self.assertEqual(p*z, p)
                self.assertEqual(q*z, q)
                self.assertEqual(z*p, p)
                self.assertEqual(z*q, q)
                self.assertEqual(repr(p*q), 'TuplePowers(%s)'%repr(rt))

    def test_equal_self(self):
        for eg in self.examples:
            p = TuplePowers(eg)
            self.assertEqual(p, p)

    def test_less_equal_self(self):
        for eg in self.examples:
            p = TuplePowers(eg)
            self.assertTrue(p<=p)

    def test_greater_equal_self(self):
        for eg in self.examples:
            p = TuplePowers(eg)
            self.assertTrue(p>=p)

    def test_not_greater_self(self):
        for eg in self.examples:
            p = TuplePowers(eg)
            self.assertTrue(not (p>p))

    def test_not_less_self(self):
        for eg in self.examples:
            p = TuplePowers(eg)
            self.assertTrue(not (p<p))

    def test_not_not_equal_self(self):
        for eg in self.examples:
            p = TuplePowers(eg)
            self.assertTrue(not (p!=p))

    def test_equal_other_same(self):
        for eg in self.examples:
            p = TuplePowers(eg)
            self.assertEqual(p, TuplePowers(eg))

    def test_diff(self):
        for eg in self.examples:
            p = TuplePowers(eg)
            for var in range(len(eg)):
                coeff, q = p.diff(var)
                self.assertEqual(coeff, eg[var])
                msg = repr(eg)+' -> '+repr(q)
                for j in range(len(eg)):
                    if j==var:
                        if eg[j]==0:
                            self.assertEqual(q[j], 0, msg)
                        else:
                            self.assertEqual(q[j], eg[j]-1, msg)
                    else:
                        self.assertEqual(q[j], eg[j], msg)

class Diff(unittest.TestCase):

    """Diff-specific range tests."""

    def test_negative_index(self):
        for i in range(-10, 0):
            m = TuplePowers()
            self.assertRaises(IndexError, m.diff, i)

    def test_bad_index(self):
        for i in range(1, 10):
            m = TuplePowers()
            self.assertRaises(IndexError, m.diff, i)

class Pow(unittest.TestCase):

    """Pow-specific range tests."""

    def test_negative_pow(self):
        for i in range(-10, 0):
            m = TuplePowers()
            self.assertRaises(ValueError, m.__pow__, i)

def suite():
    suites = []
    suites.append(unittest.makeSuite(TupleLike))
    suites.append(unittest.makeSuite(Default))
    suites.append(unittest.makeSuite(Examples))
    suites.append(unittest.makeSuite(Diff))
    suites.append(unittest.makeSuite(Pow))
    return unittest.TestSuite(suites)

if __name__ == "__main__":
    unittest.main(defaultTest='suite')
