# -*- coding: utf-8 -*-
"""
Created on Fri Jan 06 14:05:28 2017

@author: me
"""

import itertools
import math

__author__ = "Uli Koehler"
__license__ = "CC0 1.0 Universal"
__version__ = "1.1"

# Standard resistor sequences
e192 = [1.00, 1.01, 1.02, 1.04, 1.05, 1.06, 1.07, 1.09, 1.10, 1.11, 1.13, 1.14, 1.15,
1.17, 1.18, 1.20, 1.21, 1.23, 1.24, 1.26, 1.27, 1.29, 1.30, 1.32, 1.33, 1.35, 1.37,
1.38, 1.40, 1.42, 1.43, 1.45, 1.47, 1.49, 1.50, 1.52, 1.54, 1.56, 1.58, 1.60, 1.62,
1.64, 1.65, 1.67, 1.69, 1.72, 1.74, 1.76, 1.78, 1.80, 1.82, 1.84, 1.87, 1.89, 1.91,
1.93, 1.96, 1.98, 2.00, 2.03, 2.05, 2.08, 2.10, 2.13, 2.15, 2.18, 2.21, 2.23, 2.26,
2.29, 2.32, 2.34, 2.37, 2.40, 2.43, 2.46, 2.49, 2.52, 2.55, 2.58, 2.61, 2.64, 2.67,
2.71, 2.74, 2.77, 2.80, 2.84, 2.87, 2.91, 2.94, 2.98, 3.01, 3.05, 3.09, 3.12, 3.16,
3.20, 3.24, 3.28, 3.32, 3.36, 3.40, 3.44, 3.48, 3.52, 3.57, 3.61, 3.65, 3.70, 3.74,
3.79, 3.83, 3.88, 3.92, 3.97, 4.02, 4.07, 4.12, 4.17, 4.22, 4.27, 4.32, 4.37, 4.42,
4.48, 4.53, 4.59, 4.64, 4.70, 4.75, 4.81, 4.87, 4.93, 4.99, 5.05, 5.11, 5.17, 5.23,
5.30, 5.36, 5.42, 5.49, 5.56, 5.62, 5.69, 5.76, 5.83, 5.90, 5.97, 6.04, 6.12, 6.19,
6.26, 6.34, 6.42, 6.49, 6.57, 6.65, 6.73, 6.81, 6.90, 6.98, 7.06, 7.15, 7.23, 7.32,
7.41, 7.50, 7.59, 7.68, 7.77, 7.87, 7.96, 8.06, 8.16, 8.25, 8.35, 8.45, 8.56, 8.66,
8.76, 8.87, 8.98, 9.09, 9.20, 9.31, 9.42, 9.53, 9.65, 9.76, 9.88]

e96 = [1.00, 1.02, 1.05, 1.07, 1.10, 1.13, 1.15, 1.18, 1.21, 1.24, 1.27, 1.30, 1.33, 1.37, 1.40,
1.43, 1.47, 1.50, 1.54, 1.58, 1.62, 1.65, 1.69, 1.74, 1.78, 1.82, 1.87, 1.91, 1.96, 2.00,
2.05, 2.10, 2.15, 2.21, 2.26, 2.32, 2.37, 2.43, 2.49, 2.55, 2.61, 2.67, 2.74, 2.80, 2.87,
2.94, 3.01, 3.09, 3.16, 3.24, 3.32, 3.40, 3.48, 3.57, 3.65, 3.74, 3.83, 3.92, 4.02, 4.12,
4.22, 4.32, 4.42, 4.53, 4.64, 4.75, 4.87, 4.99, 5.11, 5.23, 5.36, 5.49, 5.62, 5.76, 5.90,
6.04, 6.19, 6.34, 6.49, 6.65, 6.81, 6.98, 7.15, 7.32, 7.50, 7.68, 7.87, 8.06, 8.25, 8.45,
8.66, 8.87, 9.09, 9.31, 9.53, 9.76]

e48 = [1.00, 1.05, 1.10, 1.15, 1.21, 1.27, 1.33, 1.40, 1.47, 1.54, 1.62, 1.69,
1.78, 1.87, 1.96, 2.05, 2.15, 2.26, 2.37, 2.49, 2.61, 2.74, 2.87, 3.01,
3.16, 3.32, 3.48, 3.65, 3.83, 4.02, 4.22, 4.42, 4.64, 4.87, 5.11, 5.36,
5.62, 5.90, 6.19, 6.49, 6.81, 7.15, 7.50, 7.87, 8.25, 8.66, 9.09, 9.53]

e24 = [1.0, 1.1, 1.2, 1.3, 1.5, 1.6, 1.8, 2.0, 2.2, 2.4, 2.7, 3.0,
3.3, 3.6, 3.9, 4.3, 4.7, 5.1, 5.6, 6.2, 6.8, 7.5, 8.2, 9.1]
e12 = [1.0, 1.2, 1.5, 1.8, 2.2, 2.7, 3.3, 3.9, 4.7, 5.6, 6.8, 8.2]


def getResistorRange(multiplicator, sequence=e96):
    "Get a single E96 range of resistors, e.g. for 1k use multiplicator = 1000"
    return [val*multiplicator for val in sequence]

def getStandardResistors(minExp=-1, maxExp=9, sequence=e96):
    "Get a list of all standard resistor values from 100mOhm up to 976 MOhm in Ohms"
    exponents = list(itertools.islice(itertools.count(minExp, 1), 0, maxExp - minExp))
    multiplicators = [10**x for x in exponents]
    return itertools.chain(*[getResistorRange(r, sequence=sequence) for r in multiplicators])

def findNearestResistor(value, sequence=e96):
    "Find the standard reistor value with the minimal difference to the given value"

    return min(getStandardResistors(sequence=sequence), key=lambda r: abs(value - r))

def _formatWithSuffix(v, suffix):
    """
    Format a given value with a given suffix.
    This helper function formats the value to 3 visible digits.
    v must be pre-multiplied by the factor implied by the suffix

    >>> _formatWithSuffix(1.01, "A")
    '1.01 A'
    >>> _formatWithSuffix(1, "A")
    '1.00 A'
    >>> _formatWithSuffix(101, "A")
    '101 A'
    >>> _formatWithSuffix(99.9, "A")
    '99.9 A'
    """
    if v < 10:
        res = "%.2f" % v
    elif v < 100:
        res = "%.1f" % v
    else:  # Should only happen if v < 1000
        res = "%d" % int(v)
    #Avoid appending whitespace if there is no suffix
    if suffix:
        return "%s %s" % (res, suffix)
    else:
        return res

def formatValue(v, unit=""):
    """
    Format v using SI suffices with optional units.
    Produces a string with 3 visible digits.

    >>> formatValue(1.0e-15, "V")
    '1.00 fV'
    >>> formatValue(234.6789e-3, "V")
    '234 mV'
    >>> formatValue(234.6789, "V")
    '234 V'
    >>> formatValue(2345.6789, "V")
    '2.35 kV'
    >>> formatValue(2345.6789e6, "V")
    '2.35 GV'
    >>> formatValue(2345.6789e12, "V")
    '2.35 EV'
    """
    suffixMap = {
        -5: "f", -4: "p", -3: "n", -2: "μ", -1: "m",
        0: "", 1: "k", 2: "M", 3: "G", 4: "T", 5: "E"
    }
    #Suffix map is indexed by one third of the decadic logarithm.
    exp = 0 if v == 0.0 else math.log(v, 10.0)
    suffixMapIdx = int(math.floor(exp / 3.0))
    #Ensure we're in range
    if suffixMapIdx < -5:
        suffixMapIdx = -5
    elif suffixMapIdx > 5:
        suffixMapIdx = 5
    #Pre-multiply the value
    v = v * (10.0 ** -(suffixMapIdx * 3))
    #Delegate the rest of the task to the helper
    return _formatWithSuffix(v, suffixMap[suffixMapIdx] + unit)


def formatResistorValue(v):
    return formatValue(v, unit="Ω")

# Usage example: Find and print the E48 resistor closest to 5 kOhm
#print(formatResistorValue(findNearestResistor(5000, sequence=e48)))


#parallel guy




"""due to the layout of the circuit, the resistance of the probe must be
reduced to that of the balancing resistor, meaning that the closest balance
is not appropriate: the closest value lower than Rp must be used"""

def floorCorrection(Rp,sequence):

    Rb=findNearestResistor(Rp, sequence=sequence)
    count=0
    print 'closest value was {0}'.format(Rb)

    while Rb>Rp:
        print 'value higher than probe resistance'
        count+=1
        Rb=findNearestResistor(Rp-count, sequence=sequence)

    if count==0:
        print 'closest value was appropriate'
    else:
        print 'closest value was too high, using next lowest:'
        print Rb

    return Rb
