"""Tests for module gramcore.data.images"""
import os
import numpy
from PIL import Image
from PIL import ImageStat

from nose.tools import assert_equal
from nose.tools import raises

from gramcore.data import images


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


def test_fromarray_grey():
    """Coversion from array to greyscale image

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
def test_fromarray_rgb_fail():
    """Fail to covert array to RGB image, PIL doesn't support it"""
    arr = numpy.zeros((20, 10, 3), dtype='float')

    parameters = {'data': [arr]}

    images.fromarray(parameters).convert('RGB')


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

    images.load(parameters)


def test_load_png():
    """Load png fixture and check pixel color"""
    parameters = {'path': 'green-dot.png'}

    img = images.load(parameters)

    assert_equal(img.getpixel((5, 10)), (0, 255, 0))


@raises(TypeError)
def test_load_fail():
    """Fail to load file with unkown extension"""
    parameters = {'path': 'foo.bar'}

    images.load(parameters)


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
    """Fail to save file with unknown extension"""
    img = Image.new('RGB', (10, 20))

    parameters = {'path': 'foo.bar', 'data': [img]}

    images.save(parameters)


def test_synth_positions():
    """Check synth positions with a large background and small patches"""
    background = Image.new('RGB', (30, 20))
    patch_1 = Image.new('RGB', (10, 10))
    patch_2 = Image.new('RGB', (20, 5))

    parameters = {'data': [background, patch_1, patch_2]}

    positions = images.synth_positions(parameters)

    assert_equal(positions[0][0], 0)
    assert_equal(positions[0][1], 5)
    assert_equal(positions[1][0], 10)
    assert_equal(positions[1][1], 5)


@raises(ValueError)
def test_synth_positions_small_width():
    """Fail in synth_positions because of small backgound width"""
    background = Image.new('RGB', (20, 20))
    patch_1 = Image.new('RGB', (10, 20))
    patch_2 = Image.new('RGB', (11, 20))

    parameters = {'data': [background, patch_1, patch_2]}

    positions = images.synth_positions(parameters)


@raises(ValueError)
def test_synth_positions_small_height():
    """Fail in synth_positions because of small backgound height"""
    background = Image.new('RGB', (20, 20))
    patch_1 = Image.new('RGB', (10, 21))
    patch_2 = Image.new('RGB', (10, 21))

    parameters = {'data': [background, patch_1, patch_2]}

    positions = images.synth_positions(parameters)


def test_synthetic():
    """Create a synthetic image and check for size and color assignment

    The two first patches will overlap and the last will be cropped. Notice,
    that overlapping patches overwrite each other and that patches partially
    outside the background are simply cropped and not return an error.
    """
    background = Image.new('RGB', (100, 50), (125, 125, 125))
    red = Image.new('RGB', (10, 5), (255, 0, 0))
    green = Image.new('RGB', (5, 5), (0, 255, 0))
    blue = Image.new('RGB', (20, 5), (0, 0, 255))
    positions = [
        [0, 0],
        [9, 5],
        [99, 20]
    ]

    parameters = {
        'data': [background, red, green, blue],
        'positions': positions
    }

    synth = images.synthetic(parameters)

    assert_equal(synth.size, (100, 50))
    assert_equal(synth.getpixel((0, 0)), (255, 0, 0, 255))
    # if there was no overwrite of overlapping patches, this should be:
    # assert_equal(synth.getpixel((9, 5)), (255, 255, 0, 255))
    # but since green is pasted last it is:
    assert_equal(synth.getpixel((9, 5)), (0, 255, 0, 255))


def test_synthetic_auto():
    """Create a synthetic image with automatic positions"""
    background = Image.new('RGB', (7, 3), (125, 125, 125))
    red = Image.new('RGB', (1, 1), (255, 0, 0))
    green = Image.new('RGB', (1, 1), (0, 255, 0))
    blue = Image.new('RGB', (1, 1), (0, 0, 255))

    parameters = {
        'data': [background, red, green, blue],
        'positions': 'auto'
    }

    synth = images.synthetic(parameters)

    assert_equal(synth.size, (7, 3))
    assert_equal(synth.getpixel((1, 1)), (255, 0, 0, 255))
    assert_equal(synth.getpixel((3, 1)), (0, 255, 0, 255))
    assert_equal(synth.getpixel((5, 1)), (0, 0, 255, 255))


@raises(ValueError)
def test_synthetic_less_positions():
    """Fail to create synthetic image, less positions than patches"""
    background = Image.new('RGB', (100, 50))
    patch = Image.new('RGB', (10, 10))
    positions = []

    parameters = {
        'data': [background, patch],
        'positions': positions
    }

    images.synthetic(parameters)


@raises(ValueError)
def test_synthetic_more_positions():
    """Fail to create synthetic image, more positions than patches"""
    background = Image.new('RGB', (100, 50))
    patch = Image.new('RGB', (10, 10))
    positions = [
        [5, 5],
        [9, 5]
    ]

    parameters = {
        'data': [background, patch],
        'positions': positions
    }

    images.synthetic(parameters)


def test_tiled():
    """Create a tiled image and check for size and color assignment"""
    size = [25, 25]
    img = Image.new('RGB', (10, 10))
    img.putpixel((5, 5), (0, 255, 0))

    parameters = {'data': [img], 'size': size}

    tiled = images.tiled(parameters)

    assert_equal(tiled.size, tuple(size))
    assert_equal(tiled.getpixel((5, 5)), (0, 255, 0))
    assert_equal(tiled.getpixel((15, 5)), (0, 255, 0))
