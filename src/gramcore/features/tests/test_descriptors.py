"""Tests for module gramcore.features.descriptors"""
import numpy

from nose.tools import assert_equal

from gramcore.features import descriptors


def test_hog():
    """Create a fixture and check hog result

    """
    pixels_per_cell = (9, 9)
    cells_per_block = (4, 4)
    blocks = (2, 2)

    arr_dim = pixels_per_cell[0] * cells_per_block[0] * blocks[0]
    arr = numpy.zeros((arr_dim, arr_dim))

    # put some values in the first cell
    cell = numpy.arange(81)
    cell.shape = (9, 9)
    arr[0:9, 0:9] = cell

    parameters = {'data': [arr],
                  'orientations': 8,
                  'pixels_per_cell': pixels_per_cell,
                  'cells_per_block': cells_per_block}

    results = descriptors.hog(parameters)

    # fix this after investigating how it works
    assert False

