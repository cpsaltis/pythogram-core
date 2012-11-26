"""Tests for module gramcore.datasets.surfaces"""
import numpy
from gramcore.datasets import surfaces

from nose.tools import assert_equal


def test_dtm():
    """Creates a DTM and checks size and values."""
    slope_step = 1.0
    min_value = 0.0
    size = (10, 10)
    parameters = {
        'slope_step': slope_step,
        'min_value': min_value,
        'size': size
    }

    dtm = surfaces.dtm(parameters)

    row_values = numpy.arange(min_value, size[1], slope_step)
    assert_equal(dtm.shape, size)
    assert_equal(dtm[0, 0], min_value)
    assert_equal(dtm[0, size[1] - 1], row_values[-1])
    assert_equal(dtm.sum(), row_values.sum() * size[0])
