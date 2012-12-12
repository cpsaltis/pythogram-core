"""Tests for module gramcore.features.points"""
import numpy

from nose.tools import assert_equal

from gramcore.features import points


def test_harris():
    """Create a fixture and check harris result

    The fixture is a 5x5 square, thus harris should detect 4 points on its
    corners.

    """
    arr = numpy.zeros((10, 10))
    # a 5x5 white square
    arr[3:8, 3:8] = 255

    parameters = {'data': [arr], 'min_distance': 1}

    results = points.harris(parameters)

    assert_equal(results.sum(), 4)
    assert_equal(results[4, 4], 1)
    assert_equal(results[4, 6], 1)
    assert_equal(results[6, 4], 1)
    assert_equal(results[6, 6], 1)
