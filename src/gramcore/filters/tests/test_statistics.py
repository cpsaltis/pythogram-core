"""Tests for module gramcore.filters.statistics"""
import os
import numpy

from nose.tools import assert_equal

from skimage import io

from gramcore.filters import statistics


def test_maximum():
    """Create a fixture and check the local maximum"""
    arr = numpy.zeros((11, 11))
    # a 5x5 patch
    arr[4:9, 4:9] = 1
    arr[6, 6] = 2

    parameters = {'data': [arr], 'size': [3, 3]}

    result = statistics.maximum(parameters)

    # around 2 all values will be 2 (2*9)
    # 1s will expand to their nearest neighbours (4*6) so in total
    # 5*5 + 4*6 + 2*9 - 9(don't calculate old values twice)
    assert_equal(result.sum(), 58)


def test_mean():
    """Create a fixture and check the local average"""
    arr = numpy.zeros((5, 5))
    # a 5x5 patch
    arr[1:2, 1:4] = 1.0
    arr[2:3, 1:4] = 2.0
    arr[3:4, 1:4] = 3.0

    parameters = {'data': [arr], 'size': [3, 3]}

    result = statistics.average(parameters)

    assert_equal(result[2, 2], 2.0)
    assert_equal(result[1, 2], 1.0)
    # test how reflect works, it should copy the last line outside the border
    # thus [3 3 3, 0 0 0, 0 0 0] with an average of 1
    assert_equal(result[4, 2], 1.0)


def test_median():
    """Create a fixture and check the local median"""
    arr = numpy.zeros((5, 5))
    # a 5x5 patch
    arr[1:2, 1:4] = 1
    arr[2:3, 1:4] = 2
    arr[3:4, 1:4] = 3

    parameters = {'data': [arr], 'size': [3, 3]}

    result = statistics.median(parameters)

    assert_equal(result[2, 2], 2)


def test_minimum():
    """Create a fixture and check the local minimum"""
    arr = numpy.zeros((11, 11))
    arr[4:9, 4:9] = 255
    arr[6, 6] = 0

    parameters = {'data': [arr], 'size': [3, 3]}

    result = statistics.minimum(parameters)

    assert_equal(result.sum(), 0)


def test_stddev():
    """Create a fixture and check the local standard deviation"""
    arr = numpy.zeros((5, 5))
    # a 5x5 patch
    arr[1:4, 1:4] = 1

    parameters = {'data': [arr], 'size': [3, 3]}

    result = statistics.stddev(parameters)

    assert_equal(result[2, 2], 0.0)
