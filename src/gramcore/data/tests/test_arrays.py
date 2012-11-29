"""Tests for module gramcore.data.arrays"""
import os
import numpy
from PIL import Image

from nose.tools import assert_equal
from nose.tools import raises

from gramcore.data import arrays


def setup():
    """Create array fixtures for test_load_*"""
    arr = numpy.zeros((20, 10), dtype='float')
    arr[10, 5] = 249.67
    numpy.savetxt('array.txt', arr)
    numpy.save('array.npy', arr)


def teardown():
    """Delete fixtures and test_save_* outputs"""
    os.remove('array.txt')
    os.remove('array.npy')


def test_asarray_grey():
    """Coversion from greyscale image to array

    It checks for correct shape and value assignment.

    The background color is set by default to black (value == 0). In general
    width == columns == xx' and height == rows == yy'. An 'L' image of size
    (10, 20) will become an array of shape (20, 10)
    """
    img = Image.new('L', (10, 20))
    img.putpixel((5, 10), (255))
    parameters = {'data': [img]}
    arr = arrays.asarray(parameters)
    assert_equal(arr.shape, (20, 10))
    assert_equal(arr[10, 5], 255)
    assert_equal(arr.sum(), 255)


def test_asarray_rgb():
    """Coversion from RGB image to array

    It checks for correct shape and value assignment. An 'RGB' image of size
    (10, 20) will become an array of shape (20, 10, 3). [:, :, 0] will be the
    red channel 1 the green and 2 the blue.
    """
    img = Image.new('RGB', (10, 20))
    img.putpixel((5, 10), (255, 0, 0))
    parameters = {'data': [img]}
    arr = arrays.asarray(parameters)
    assert_equal(arr.shape, (20, 10, 3))
    assert_equal(arr[10, 5, 0], 255)
    assert_equal(arr.sum(), 255)


def test_load_txt():
    """Load txt fixture and check value"""
    parameters = {'path': 'array.txt'}
    arr = arrays.load(parameters)
    assert_equal(arr[10, 5], 249.67)
    assert_equal(arr.sum(), 249.67)


def test_load_npy():
    """Load npy fixture and check value"""
    parameters = {'path': 'array.npy'}
    arr = arrays.load(parameters)
    assert_equal(arr[10, 5], 249.67)
    assert_equal(arr.sum(), 249.67)


@raises(TypeError)
def test_load_fail():
    """Fail to load file with unkown extension"""
    parameters = {'path': 'foo.bar'}
    arrays.load(parameters)


def test_save_txt():
    """Save 2D array to txt"""
    arr = numpy.zeros((20, 10), dtype='float')
    parameters = {'path': 'array.txt', 'data': [arr]}
    assert arrays.save(parameters)


@raises(TypeError)
def test_save_txt_fail():
    """Fail to save 3D array to txt, numpy doesn't support it"""
    arr = numpy.zeros((20, 10, 3), dtype='float')
    parameters = {'path': 'array.txt', 'data': [arr]}
    arrays.save(parameters)


def test_save_npy():
    """Save 2D array to npy"""
    arr = numpy.zeros((20, 10), dtype='float')
    parameters = {'path': 'array.npy', 'data': [arr]}
    assert arrays.save(parameters)


def test_save_npy_3d():
    """Save 3D array to npy"""
    arr = numpy.zeros((20, 10, 3), dtype='float')
    arr[10, 5, 1] = 249.49
    parameters = {'path': 'array.npy', 'data': [arr]}
    assert arrays.save(parameters)
    arr = numpy.load('array.npy')
    assert_equal(arr[10, 5, 1], 249.49)
    assert_equal(arr.sum(), 249.49)


@raises(TypeError)
def test_save_fail():
    """Fail to save file with unkown extension"""
    arr = numpy.zeros((20, 10), dtype='float')
    parameters = {'path': 'foo.bar', 'data': [arr]}
    arrays.save(parameters)


def test_dtm():
    """Create a DTM and checks size and values."""
    slope_step = 1.0
    min_value = 0.0
    size = (10, 10)

    parameters = {
        'slope_step': slope_step,
        'min_value': min_value,
        'size': size
    }

    dtm = arrays.dtm(parameters)

    # this is a fixture of a row as it should be generated
    row_values = numpy.arange(min_value, size[1], slope_step)

    assert_equal(dtm.shape, size)
    assert_equal(dtm[0, 0], min_value)
    assert_equal(dtm[0, size[1] - 1], row_values[-1])
    assert_equal(dtm.sum(), row_values.sum() * size[0])
