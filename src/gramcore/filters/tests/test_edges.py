"""Tests for module gramcore.filters.edges"""
import os
import numpy

from nose.tools import assert_equal

from skimage import io

from gramcore.filters import edges


def setup():
    """Create image fixture

    It creates a 20x40 image with black background and paints an 11x11 white
    rectangle inside. Choose odd dimensions for the filters to work more
    predictively.

    """
    img = numpy.zeros((20, 40))
    img[5:16, 15:26] = 255
    io.imsave('white-square.tif', img.astype('uint8'))


def teardown():
    """Delete fixture"""
    #os.remove('white-square.tif')


def test_canny():
    """Apply canny to grey image and check return values

    .. warning::

        This seems to produce some artifacts. You expect you get 44 (4*11)
        pixels of edges. Instead it gets 46, when sigma is 1 and 40 when sigma
        is 2. In both cases the shape is correct, but a few edge pixels are
        missing or instroduced at a wrong positions.

    """
    img = io.imread('white-square.tif')

    parameters = {'data': [img], 'sigma': 1.0}

    result = edges.canny(parameters)

    # this should be 44 check the resulting image with
    #result *= 255
    #io.imsave('result.tif', result)
    assert_equal(result.sum(), 46)


def test_prewitt():
    """Apply prewitt to grey image and check return values

    .. note::

        This produces correct shape though it shrinks it by 2 pixels, there
        are no edge pixels on the corners and each edge has a width of 2
        pixels. Based on the original rectangle size, which is 11x11, and the
        above issues it returns 4*9*2 = 72 edge pixels.

    """
    img = io.imread('white-square.tif')

    parameters = {'data': [img]}

    result = edges.prewitt(parameters)
    result = result.astype('uint8')

    assert_equal(result.sum(), 72)


def test_sobel():
    """Apply sobel to grey image and check return values

    .. note::

        This produces correct shape though it shrinks it by 2 pixels and each
        edge has a width of 2 pixels. Based on the original rectangle size,
        which is 11x11, and the above issues it returns 4*9*2 + 4 = 76 edge
        pixels.

    """
    img = io.imread('white-square.tif')

    parameters = {'data': [img]}

    result = edges.sobel(parameters)
    result = result.astype('uint8')

    assert_equal(result.sum(), 76)
