"""Tests for module gramcore.operations.images"""
import os
import numpy
from PIL import Image
from PIL import ImageStat
from gramcore.operations import images

from nose.tools import assert_equal
from nose.tools import raises


def setup():
    """Create image fixtures for test_load_*

    To create an image PIL requires size (width, height in pixels) and mode
    ('L', 'RGB', etc). The background color is set by default to black
    (value == 0). Color values in RGB images are stored in (R, G, B) order.
    """
    img = Image.new('RGB', (10, 20))
    img.putpixel((5, 10), (0, 255, 0))
    img.save('green-dot.tif')
    img.save('green-dot.jpg')
    img.save('green-dot.png')


def teardown():
    """Delete fixtures and test_save_* outputs"""
    os.remove('green-dot.tif')
    os.remove('green-dot.jpg')
    os.remove('green-dot.png')


def test_fromarray_L():
    """Coversion from array to L image

    Checks for correct shape, value assignment and type conversion.

    In general width == columns == xx' and height == rows == yy'. A 2D array
    will be converted to an image of mode '1', L' or 'F'. If the array has a
    shape of (20, 10) the resulting image will have size (10, 20).

    .. warning::

        Converting from array of floats to 'L' image will reduce accuracy. 'F'
        images are usually not recognized from viewers and create problems
        with image stats. Notice below that only rounding ensures assertions.
    """
    arr = numpy.zeros((20, 10), dtype='float')
    arr[10, 5] = 249.34

    parameters = {'data': [arr]}

    img = images.fromarray(parameters).convert('L')
    stats = ImageStat.Stat(img)

    assert_equal(img.size, (10, 20))
    assert_equal(img.getpixel((5, 10)), round(arr[10, 5]))
    assert_equal(stats.sum[0], round(arr.sum()))


@raises(TypeError)
def test_fromarray_RGB_fail():
    """Fail to covert array to RGB image, PIL doesn't support it"""
    arr = numpy.zeros((20, 10, 3), dtype='float')

    parameters = {'data': [arr]}

    img = images.fromarray(parameters).convert('RGB')


def test_load_tif():
    """Load tif fixture and check pixel color"""
    parameters = {'path': 'green-dot.tif'}

    img = images.load(parameters)

    assert_equal(img.getpixel((5, 10)), (0, 255, 0))


def test_load_jpg():
    """Load jpg fixture

    Can't check for color here, because compression changes it.
    """
    parameters = {'path': 'green-dot.jpg'}

    img = images.load(parameters)


def test_load_png():
    """Load png fixture and check pixel color"""
    parameters = {'path': 'green-dot.png'}

    img = images.load(parameters)

    assert_equal(img.getpixel((5, 10)), (0, 255, 0))


def test_resize_smaller():
    """Resize an image to smaller size"""
    img_before = Image.new('L', (10, 20))
    img_before.putpixel((0, 0), (255))
    size = (5, 10)

    parameters = {'data': [img_before], 'width': size[0], 'height': size[1]}

    img_after = images.resize(parameters)
    arr = numpy.asarray(img_after)

    assert_equal(img_after.getpixel((0, 0)), (255))
    assert_equal(img_after.size, size)
    assert_equal(arr.sum(), 255)


def test_resize_larger():
    """Resize an image to larger size"""
    img_before = Image.new('L', (10, 20))
    img_before.putpixel((0, 0), (255))
    size = (20, 40)

    parameters = {'data': [img_before], 'width': size[0], 'height': size[1]}

    img_after = images.resize(parameters)
    arr = numpy.asarray(img_after)

    assert_equal(img_after.getpixel((0, 0)), (255))
    assert_equal(img_after.getpixel((1, 0)), (255))
    assert_equal(img_after.getpixel((0, 1)), (255))
    assert_equal(img_after.getpixel((1, 1)), (255))
    assert_equal(img_after.size, size)
    assert_equal(arr.sum(), 4 * 255)


def test_rotate_noexpand():
    """Rotate an image without expanding

    When rotating without expanding pixels on the border get cropped.
    """
    size = (10, 20)
    img_before = Image.new('L', size)
    img_before.putpixel((0, 0), (255))

    parameters = {'data': [img_before], 'angle': 45}

    img_after = images.rotate(parameters)
    arr = numpy.asarray(img_after)

    assert_equal(img_after.size, size)
    assert_equal(arr.sum(), 0)


def test_rotate_expand():
    """Rotate an image with expanding

    TODO: make this more generic, not tied to certain size
    """
    size = (11, 21)
    img_before = Image.new('L', size)
    img_before.putpixel((0, 0), (255))

    parameters = {'data': [img_before], 'angle': 45, 'expand': 1}

    img_after = images.rotate(parameters)

    assert_equal(img_after.getpixel((1, 8)), (255))
    assert_equal(img_after.size, (23, 23))


@raises(TypeError)
def test_load_fail():
    """Fail to load file with unkown extension"""
    parameters = {'path': 'foo.bar'}

    img = images.load(parameters)


def test_save_tif():
    """Save image to tif"""
    img = Image.new('RGB', (10, 20))

    parameters = {'path': 'green-dot.tif', 'data': [img]}

    assert images.save(parameters)


def test_save_jpg():
    """Save image to jpg"""
    img = Image.new('RGB', (10, 20))

    parameters = {'path': 'green-dot.jpg', 'data': [img]}

    assert images.save(parameters)


def test_save_png():
    """Save image to png"""
    img = Image.new('RGB', (10, 20))

    parameters = {'path': 'green-dot.png', 'data': [img]}

    assert images.save(parameters)


@raises(TypeError)
def test_save_fail():
    """Fail to save file with unkown extension"""
    img = Image.new('RGB', (10, 20))

    parameters = {'path': 'foo.bar', 'data': [img]}

    images.save(parameters)
