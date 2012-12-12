"""Feature descriptors usefull in bag of features approaches.

These are applied to numpy.arrays representing images.

"""
import numpy
from skimage import feature


def hog(parameters):
    """Extracts histograms of oriented gradients.

    It wraps `skimage.feature.hog`. The `visualise` and `normalise` options
    are not supported.

    It works for greyscale images and assigns the values to each pixel of the
    cell/block it belongs to.

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

    :return: numpy.array, it contains 1s where points were found, otherwise 0

    (TODO: investigate the algorithm and return values, how do
    pixels_per_cell and cells_per_block relate, how do you assign the returned
    values to image pixels, fix the test too)

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
