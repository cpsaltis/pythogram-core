"""Tests for module gramcore.transformations.geometric"""
import numpy

from nose.tools import assert_equal

from gramcore.transformations import geometric


def test_resize_grey():
    """Enlarge grey image, check new size and intensities"""
    data = numpy.zeros((5, 5))
    data[2, 2] = 255
    output_shape = (10, 10)

    parameters = {'data': [data], 'output_shape': output_shape}

    resized = geometric.resize(parameters)

    assert_equal(resized.shape, output_shape)
    assert_equal(resized[4, 4], 1)
    assert_equal(resized.sum(), 16)


def test_resize_rgb():
    """Enlarge rgb image, check new size and intensities"""
    data = numpy.zeros((5, 5, 3))
    data[2, 2, 1] = 255
    output_shape = (10, 10)

    parameters = {'data': [data], 'output_shape': output_shape}

    resized = geometric.resize(parameters)

    assert_equal(resized.shape, (10, 10, 3))
    assert_equal(resized[4, 4, 0], 0)
    assert_equal(resized[4, 4, 1], 1)
    assert_equal(resized[4, 4, 2], 0)
    assert_equal(resized.sum(), 16)


def test_rotate_grey_noexpand():
    """Rotate grey image without expanding, check new size and intensities"""
    data = numpy.zeros((5, 5))
    data[2, 2] = 255
    angle = 45

    parameters = {'data': [data], 'angle': angle}

    rotated = geometric.rotate(parameters)

    assert_equal(rotated.sum(), 5)
    # These should replace the following when skimage fixes the resize issue
    #assert_equal(rotated.sum(), 4)
    #assert_equal(rotated.shape, (5, 5))
    #assert_equal(rotated[2, 2], 1)
    assert_equal(rotated.shape, (7, 7))
    assert_equal(rotated[3, 3], 1)


def test_rotate_grey_expand():
    """Rotate grey image and expand it, check new size and intensities"""
    data = numpy.zeros((5, 5))
    data[2, 2] = 255
    angle = 45
    resize = True

    parameters = {'data': [data], 'angle': angle, 'resize': resize}

    rotated = geometric.rotate(parameters)

    assert_equal(rotated.sum(), 5)
    # These should replace the following when skimage fixes the resize issue
    #assert_equal(rotated.shape, (7, 7))
    #assert_equal(rotated[3, 3], 1)
    assert_equal(rotated.shape, (5, 5))
    assert_equal(rotated[2, 2], 1)


def test_rotate_rgb_noexpand():
    """Rotate rgb image without expanding, check new size and intensities"""
    data = numpy.zeros((5, 5, 3))
    data[2, 2, 1] = 255
    angle = 45

    parameters = {'data': [data], 'angle': angle}

    rotated = geometric.rotate(parameters)

    assert_equal(rotated.sum(), 5)
    # These should replace the following when skimage fixes the resize issue
    #assert_equal(rotated.shape, (5, 5, 3))
    #assert_equal(rotated[2, 2, 0], 0)
    #assert_equal(rotated[2, 2, 1], 1)
    #assert_equal(rotated[2, 2, 0], 0)
    assert_equal(rotated.shape, (7, 7, 3))
    assert_equal(rotated[3, 3, 0], 0)
    assert_equal(rotated[3, 3, 1], 1)
    assert_equal(rotated[3, 3, 2], 0)


def test_rotate_rgb_expand():
    """Rotate rgb image and expand it, check new size and intensities"""
    data = numpy.zeros((5, 5, 3))
    data[2, 2, 1] = 255
    angle = 45
    resize = True

    parameters = {'data': [data], 'angle': angle, 'resize': resize}

    rotated = geometric.rotate(parameters)

    assert_equal(rotated.sum(), 5)
    # These should replace the following when skimage fixes the resize issue
    #assert_equal(rotated.shape, (7, 7, 3))
    #assert_equal(rotated[3, 3, 0], 0)
    #assert_equal(rotated[3, 3, 1], 1)
    #assert_equal(rotated[3, 3, 0], 0)
    assert_equal(rotated.shape, (5, 5, 3))
    assert_equal(rotated[2, 2, 0], 0)
    assert_equal(rotated[2, 2, 1], 1)
    assert_equal(rotated[2, 2, 0], 0)
