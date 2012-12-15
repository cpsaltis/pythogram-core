"""Feature descriptors usefull in bag of features approaches.

These are applied to numpy.arrays representing images.

"""
import numpy
from skimage import feature


def hog(parameters):
    """Extracts histograms of oriented gradients.

    It wraps `skimage.feature.hog`. The `visualise` and `normalise` options
    are not supported.

    It works only on 2D arrays / greyscale images.

    For each cell it calculates `x` values, where `x` is the number of
    orientations asked. Cells are non-overlapping groups of pixels so e.g. if
    an image is 10x10 pixels and `pixels_per_cell` == (5, 5) the image will
    be divided to 4 cells. Blocks are local groups of cells which are used for
    normalisation, thus reducing the effects of e.g. lighting conditions.
    Blocks are in fact sliding windows upon the cells. For each such position
    of the block the algorithm returns a set of cell values.

    Supposing::

        orientations = 9
        cells_per_block = (3, 3)
        block_positions = (8, 8)

    Then the number of the returned values can be calculated with::

        nr_of_values = 9 * 3 * 3 * 8 * 8

    The results are returned per block position [TODO test if this is true].

    In the case of looking for buildings there are two options:

        1. Use a block as big as the entire image. This will lead in a global
        value normalisation which is not expected to be very accurate.

        2. Set `pixels_per_cell`, `cells_per_block` to values that approximate
        the size of the building in the image. e.g. for an 1m GSD image a
        cell of 9x9 pixels and a block of 3x3 cells can be enough to depict
        a 81m^2 building and its surroundings.

    [TODO how to return values per pixel and not per blocks/cell, which
    array layout would work best? keep in mind that each cell has values
    equal to `orientations`, thus a 3D array width depth `orientations` seems
    more appropriate.]

    :param parameters['data'][0]: input array
    :type parameters['data'][0]: numpy.array
    :param parameters['orientations]: number of oriented bins, defaults to 9
    :type parameters['orientations']: integer
    :param parameters['pixels_per_cell']: size of a cell in pixels, defaults
                                          to (8, 8)
    :type parameters['pixels_per_cell']: tuple
    :param parameters['cells_per_block']: size of a block in cells, defaults
                                          to (3, 3)
    :type parameters['cells_per_block']: tuple

    :return: numpy.array, this is currently a 1D array

    """
    data = parameters['data'][0]
    orientations = parameters.get('orientations', 9)
    pixels_per_cell = parameters.get('pixels_per_cell', [8, 8])
    cells_per_block = parameters.get('cells_per_block', [3, 3])

    hogs = feature.hog(data,
                       orientations=orientations,
                       pixels_per_cell=tuple(pixels_per_cell),
                       cells_per_block=tuple(cells_per_block))

    return hogs
