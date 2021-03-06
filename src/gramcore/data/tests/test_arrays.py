"""Tests for module gramcore.data.arrays"""
import os
import numpy
from PIL import Image

from nose.tools import assert_equal, assert_almost_equal, raises

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
    (10, 20) will become an array of shape (20, 10).

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


def test_get_shape():
    """Get array shape"""
    shape = (10, 10)
    arr = numpy.zeros(shape)

    parameters = {'data': [arr]}

    result = arrays.get_shape(parameters)

    assert_equal(result, shape)


def test_gaussian_noise():
    """Generate gaussian noise of certain dimensions

    Creates a large array and check only until the second decimal position
    to be sure that randomness will not cause test failure.

    """
    mean = 0
    stddev = 5
    shape = (1000, 1000)

    parameters = {'shape': shape, 'mean': mean, 'stddev': stddev}

    noise = arrays.gaussian_noise(parameters)

    assert_almost_equal(abs(noise.mean() - mean), 0.0, places=1)
    assert_almost_equal(abs(noise.std() - stddev), 0.0, places=1)


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


def test_split():
    """Split a 3D array and check if the correct layer is returned"""
    data = numpy.zeros((10, 10, 3))
    data[0, 0, 1] = 1
    layer = 1

    parameters = {'data': [data], 'layer': layer}

    arr = arrays.split(parameters)

    assert_equal(data[0, 0, 1], 1)
    assert_equal(data.sum(), 1)
    assert_equal(arr[0, 0], 1)
    assert_equal(arr.sum(), 1)


def test_dtm():
    """Create a DTM and check size and values."""
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


def test_dsm():
    """Create a DSM and check size and values."""
    dtm = numpy.arange(100)
    dtm.shape = (10, 10)
    mask = numpy.zeros((10, 10))
    mask[2:5, 2:5] = 1
    mask[6:9, 6:9] = 1
    delta_height = 1000

    parameters = {
        'data': [dtm, mask],
        'delta_height': delta_height
    }

    dsm = arrays.dsm(parameters)

    assert_equal(dsm.shape, dtm.shape)

    assert numpy.all(dsm[2:5, 2:5] == 1044)
    assert numpy.all(dsm[6:9, 6:9] == 1088)
    # make sure the initial array was not overwritten
    temp = numpy.arange(100)
    temp.shape = (10, 10)
    numpy.testing.assert_array_equal(dtm, temp)
    # make sure no other values where changed
    assert_equal(dsm.sum(), 23148)

