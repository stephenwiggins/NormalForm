"""

Author: Dr. Andrew David Burbanks, 2005.
This software is Copyright (C) 2004-2008  Bristol University
and is released under the GNU General Public License version 2.

"""

import unittest
import random
import io

from Powers import Powers
from Polynomial import Polynomial
from PolynomialRing import PolynomialRing
## Automatically adapted for numpy.oldnumeric Dec 16, 2008 by alter_code1.py
try:
    from numpy.oldnumeric.mlab import fabs
except:
    from MLab import fabs

from PolynomialTest import rand_poly
from PolynomialTest import _eq as _poly_eq

def _eq(a, b, tol=1.0e-8):
    """

    We need to loosen tolerance for Moyal bracket calculations.

    """
    return _poly_eq(a, b, tol)

n_cases = 4

class PolynomialRingTest(unittest.TestCase):

    def test_one(self):
        for n_vars in range(1, 7):
            ring = PolynomialRing(n_vars)
            one = ring.one()
            self.assertTrue(isinstance(one, Polynomial))
            self.assertTrue(one.n_vars() == n_vars)
            self.assertTrue(len(one) == 1)
            po, co = list(one.powers_and_coefficients())[0]
            self.assertTrue(len(po) == n_vars)
            for p in po:
                self.assertTrue(p == 0)
            self.assertTrue(co == 1.0)

    def test_zero(self):
        for n_vars in range(1, 7):
            ring = PolynomialRing(n_vars)
            zero = ring.zero()
            self.assertTrue(isinstance(zero, Polynomial))
            self.assertTrue(zero.n_vars() == n_vars)
            self.assertTrue(len(zero) == 0)
            self.assertTrue(not zero)

    def test_n_vars(self):
        for n_vars in range(1, 25):
            ring = PolynomialRing(n_vars)
            self.assertTrue(ring.n_vars() == n_vars)

    def test_coordinate_monomial(self):
        for n_vars in range(1, 7):
            ring = PolynomialRing(n_vars)
            for var in range(n_vars):
                x = ring.coordinate_monomial(var)
                self.assertTrue(isinstance(x, Polynomial))
                self.assertTrue(x.n_vars() == n_vars)
                self.assertTrue(len(x) == 1)
                po, co = list(x.powers_and_coefficients())[0]
                self.assertTrue(len(po) == n_vars)
                for i, p in enumerate(po):
                    if i == var:
                        self.assertTrue(p == 1)
                    else:
                        self.assertTrue(p == 0)
                self.assertTrue(co == 1.0)

    def test_grad(self):
        poly = Polynomial(3, {Powers((0, 0, 0)): 1.0,
                              Powers((1, 1, 0)): -2.0,
                              Powers((0, 2, 0)): 5.3,
                              Powers((0, 1, 5)): -9})
        ring = PolynomialRing(3)
        grad = ring.grad(poly)
        g0 = Polynomial(3, {Powers((0, 1, 0)): -2.0})
        g1 = Polynomial(3, {Powers((1, 0, 0)): -2.0,
                            Powers((0, 1, 0)): 10.6,
                            Powers((0, 0, 5)): -9})
        g2 = Polynomial(3, {Powers((0, 1, 4)): -45.0})
        for expected, actual in zip((g0, g1, g2), grad):
            self.assertTrue(expected == actual, (expected, actual))

def suite():
    suites = []
    suites.append(unittest.makeSuite(PolynomialRingTest))
    return unittest.TestSuite(suites)

if __name__ == '__main__':
    unittest.main(defaultTest='suite')
    
