"""Tests for module gramcore.filters.morphology"""
import numpy

from nose.tools import assert_equal

from gramcore.filters import morphology


def test_closing():
    """Create a fixture and check the result after closing"""
    arr = numpy.zeros((11, 11))
    # a 5x5 patch
    arr[4:9, 4:9] = 255
    # with a hole in the middle
    arr[6, 6] = 0

    parameters = {'data': [arr], 'size': [3, 3]}

    result = morphology.closing(parameters)

    # the hole should be closed
    assert_equal(result.sum(), 5 * 5 * 255)


def test_erosion():
    """Create a fixture and check after erosion"""
    arr = numpy.zeros((11, 11))
    # a 5x5 patch
    arr[4:9, 4:9] = 255
    # with a hole in the middle
    arr[6, 6] = 0

    parameters = {'data': [arr], 'size': [3, 3]}

    result = morphology.erosion(parameters)

    # the hole is enough to make all meighbours 0.0
    assert_equal(result.sum(), 0)


def test_dilation():
    """Create a fixture and check after dilation"""
    arr = numpy.zeros((11, 11))
    # a 5x5 patch
    arr[4:9, 4:9] = 255
    # with a hole in the middle
    arr[6, 6] = 0

    parameters = {'data': [arr], 'size': [3, 3]}

    result = morphology.dilation(parameters)

    # every cell in the initial patch and around it should now have value 255
    assert_equal(result.sum(), 7 * 7 * 255)


def test_opening():
    """Create a fixture and check after opening"""
    arr = numpy.zeros((11, 11))
    # a 5x5 patch
    arr[4:9, 4:9] = 255
    # with a hole on the edge, if you put it in the middle the erosion will
    # delete everything
    arr[4, 4] = 0

    parameters = {'data': [arr], 'size': [3, 3]}

    result = morphology.opening(parameters)

    assert_equal(result.sum(), 5 * 5 * 255 - 255)
