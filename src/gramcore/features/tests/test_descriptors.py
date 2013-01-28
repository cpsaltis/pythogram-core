"""Tests for module gramcore.features.descriptors"""
import numpy

from nose.tools import assert_equal

from gramcore.features import descriptors


def test_hog_size():
    """Create a fixture and check hog result size

    There are already enough tests in skimage for this, just adding so to
    document how many values are returned and why.

    Creates a square array and inputs it to hog. For simplicity the
    blocks and the cells are square. The calculated orientations are set to 9.
    Based on these the result should include a number of values equal to::

        block_possitions^2 * cells_per_block^2 * orientations

    HOG calculations take place in row major order.

    """
    pixels_per_cell = 9
    cells_per_block = 8
    orientations = 9

    # double the size so to generate some blocks and initialize the array
    arr_dim =  2 * pixels_per_cell * cells_per_block
    arr = numpy.zeros((arr_dim, arr_dim))

    parameters = {'data': [arr],
                  'orientations': orientations,
                  'pixels_per_cell': [pixels_per_cell, pixels_per_cell],
                  'cells_per_block': [cells_per_block, cells_per_block]}

    results = descriptors.hog(parameters)

    # calculate how many blocks fit in the array, basically how many
    # sliding window positions are there
    block_positions = (arr_dim / pixels_per_cell) - cells_per_block + 1

    assert_equal(results.shape[0], block_positions**2 *\
                                   cells_per_block**2 *\
                                   orientations)

