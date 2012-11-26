"""Tests for module gramcore.operations.arrays"""
import os
import numpy
from PIL import Image
from gramcore.operations import arrays

from nose.tools import assert_equal
from nose.tools import raises


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


def test_add_noise():
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
    noisy = arrays.add_noise(parameters)
    assert_equal(data.sum(), shape[0] * shape[1])


def test_asarray_L():
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


def test_asarray_RGB():
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
    arr = arrays.load(parameters)


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
