"""Tests for module gramcore.filters.thresholds"""
import numpy

from nose.tools import assert_equal

from gramcore.filters import thresholds


def test_binary():
    """Create a fixture and check the result after binary thresholding"""
    arr = numpy.arange(50)
    arr.shape = (5, 10)
    threshold = 48

    parameters = {'data': [arr], 'threshold': threshold}

    result = thresholds.binary(parameters)

    # the arange contains values from 0 to 49, by thresholding with 48
    # only one value should remain
    assert_equal(result.sum(), 1)


def test_otsu():
    """Create a fixture and check the result after otsu thresholding"""
    arr = numpy.arange(50)
    arr.shape = (5, 10)

    parameters = {'data': [arr]}

    result = thresholds.otsu(parameters)

    # When otsu is calculated for this range, it becomes equal to the mean
    # minus half. Thus, only half of the initial values should pass it.
    assert_equal(result.sum(), 50 / 2)
