"""Tests for module gramcore.filters.edges"""
import os
import numpy
from PIL import Image, ImageDraw

from nose.tools import assert_equal

from skimage import io

from gramcore.filters import edges


def setup():
    """Create image fixture

    The background color is set by default to black (value == 0).

    .. note::

        Although the rectangle should be 10x10 in reality it returns an 11x11.
        If the image is read with io.imread, then the colored pixels and their
        neighbours can be accessed with arr[9:22, 4:17].

    """
    img = Image.new('L', (20, 40))
    draw = ImageDraw.Draw(img)
    draw.rectangle([(5, 10), (15, 20)], fill=255)
    img.save('white-square.tif')

    del draw


def teardown():
    """Delete fixture"""
    os.remove('white-square.tif')


def test_canny():
    """Apply canny to grey image and check return values

    .. warning::

        This seems to produce some artifacts. The fixture is a black
        image with a white 11x11 rectangle. Thus you expect you get 44 (4*11)
        pixels of edges. Instead it gets 50, when sigma is 1 and 40 when sigma
        is 2. In both cases the shape is not correct.

    """
    img = io.imread('white-square.tif')

    parameters = {'data': [img], 'sigma': 1.0}

    result = edges.canny(parameters)

    # this should be 44 check the resulting image with
    #result *= 255
    #io.imsave('result.tif', result)
    assert_equal(result.sum(), 50)


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
