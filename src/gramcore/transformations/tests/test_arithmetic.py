"""Tests for module gramcore.transformations.arithmetic"""
import numpy

from nose.tools import assert_equal

from gramcore.transformations import arithmetic


def test_add_two_arrays():
    """Sum 2 arrays"""
    one = numpy.ones((10, 10))
    two = 2 * one

    parameters = {'data': [one, two]}

    result = arithmetic.add(parameters)

    assert_equal(result.sum(), 3 * 10 * 10)


def test_add_three_arrays():
    """Sum 3 arrays"""
    one = numpy.ones((10, 10))
    two = 2 * one
    three = 3 * one

    parameters = {'data': [one, two, three]}

    result = arithmetic.add(parameters)

    assert_equal(result.sum(), 6 * 10 * 10)


def test_diff():
    """Subtract arrays"""
    one = numpy.ones((10, 10))
    two = 2 * one

    parameters = {'data': [two, one]}

    result = arithmetic.diff(parameters)

    assert_equal(result.sum(), 1 * 10 * 10)


def test_divide():
    """Divide arrays"""
    one = numpy.ones((10, 10))
    two = 2 * one

    parameters = {'data': [two, one]}

    result = arithmetic.divide(parameters)

    assert_equal(result.sum(), 2 * 10 * 10)


def test_ndvi():
    """Check NDVI"""
    red = numpy.ones((10, 10))
    nir = red

    parameters = {'data': [red, nir]}

    result = arithmetic.ndvi(parameters)

    assert_equal(result.sum(), 0)
