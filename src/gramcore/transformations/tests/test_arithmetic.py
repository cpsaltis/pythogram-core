"""Tests for module gramcore.transformations.arithmetic"""
import numpy

from nose.tools import assert_equal

from gramcore.transformations import arithmetic


def test_add_gaussian_noise():
    """Add noise to an array

    Check if the initial object stays intact. Doesn't test for randomness,
    have to trust numpy in this. It would be great if something like this
    worked, but random is random...

    >>> just_noise = noisy - numpy.ones((shape))
    >>> assert_equal(just_noise.mean(), mean)
    >>> assert_equal(just_noise.std(), stddev)
    """
    mean = 10
    stddev = 5
    shape = (5, 5)
    data = numpy.ones(shape)
    parameters = {'mean': mean, 'stddev': stddev, 'data': [data]}
    noisy = arithmetic.add_gaussian_noise(parameters)
    assert_equal(data.sum(), noisy.shape[0] * noisy.shape[1])
