"""
Basic statistics module.

This module provides functions for calculating statistics of data, including
averages, variance, and standard deviation.

Calculating averages
--------------------

==================  =============================================
Function            Description
==================  =============================================
mean                Arithmetic mean (average) of data.
harmonic_mean       Harmonic mean of data.
median              Median (middle value) of data.
median_low          Low median of data.
median_high         High median of data.
median_grouped      Median, or 50th percentile, of grouped data.
mode                Mode (most common value) of data.
==================  =============================================

Calculate the arithmetic mean ("the average") of data:

>>> mean([-1.0, 2.5, 3.25, 5.75])
2.625


Calculate the standard median of discrete data:

>>> median([2, 3, 4, 5])
3.5


Calculate the median, or 50th percentile, of data grouped into class intervals
centred on the data values provided. E.g. if your data points are rounded to
the nearest whole number:

>>> median_grouped([2, 2, 3, 3, 3, 4])  #doctest: +ELLIPSIS
2.8333333333...

This should be interpreted in this way: you have two data points in the class
interval 1.5-2.5, three data points in the class interval 2.5-3.5, and one in
the class interval 3.5-4.5. The median of these data points is 2.8333...


Calculating variability or spread
---------------------------------

==================  =============================================
Function            Description
==================  =============================================
pvariance           Population variance of data.
variance            Sample variance of data.
pstdev              Population standard deviation of data.
stdev               Sample standard deviation of data.
==================  =============================================

Calculate the standard deviation of sample data:

>>> stdev([2.5, 3.25, 5.5, 11.25, 11.75])  #doctest: +ELLIPSIS
4.38961843444...

If you have previously calculated the mean, you can pass it as the optional
second argument to the four "spread" functions to avoid recalculating it:

>>> data = [1, 2, 2, 4, 4, 4, 5, 6]
>>> mu = mean(data)
>>> pvariance(data, mu)
2.5


Exceptions
----------

A single exception is defined: StatisticsError is a subclass of ValueError.

"""

__all__ = [ 'StatisticsError',
            'pstdev', 'pvariance', 'stdev', 'variance',
            'median',  'median_low', 'median_high', 'median_grouped',
            'mean', 'mode', 'harmonic_mean',
          ]

from collections import Counter
from math import sqrt

def mean(data):
    return sum(data) / len(data)

def harmonic_mean(data):
    raise NotImplementedError


def median(data):
    _data = sorted(data)
    l = len(_data)
    if l % 2 == 0:
        _median = (_data[l//2] + _data[l//2-1]) / 2
    else:
        _median = _data[l//2]
    return _median

def median_low(data):
    _data = sorted(data)
    l = len(_data)
    if l % 2 == 0:
        _median = _data[l//2-1]
    else:
        _median = _data[l//2]
    return _median


def median_high(data):
    _data = sorted(data)
    l = len(_data)
    if l % 2 == 0:
        _median = _data[l//2]
    else:
        _median = _data[l//2]
    return _median


def median_grouped(data):
    return median(data)

def mode(data):
    counter = Counter(data)
    max_count = max(counter.values())
    _mode = [k for k,v in counter.items() if v == max_count]
    if len(_mode) > 1:
        raise ValueError("No Unique Mode, found {} equally common values".format(len(_mode)))
    else:
        return _mode[0]


def variance(data):
    average=mean(data)
    _variance=0
    for d in data:
        _variance += ((average-d)**2)
        final_variance=_variance/len(data)
    return final_variance

def pvariance(data):
    average=mean(data)
    _variance=0
    for d in data:
        _variance += ((average-d)**2)
        final_variance=_variance/len(data)
    return final_variance

def variance(data):
    average=mean(data)
    _variance=0
    for d in data:
        _variance += ((average-d)**2)
        final_variance=_variance/(len(data) -1)
    return final_variance

def pstdev(data):
    return sqrt(pvariance(data))

def stdev(data):
    return sqrt(variance(data))

