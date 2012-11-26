"""Generates artificial raster data that represent surfaces.

These are just numpy.arrays so they can be handled with functions from
core.operations.arrays.
"""
import numpy
from scipy.ndimage import measurements


def dtm(parameters):
    """Generates a dtm with linear slope.

    Slope is applied in row major order, so pixels in each row have the same
    height value.

    :param parameters['slope_step']: dH/pixel
    :type parameters['slope_step']: float or integer
    :param parameters['min_value']: global minimum height value
    :type parameters['min_value']: float or integer
    :param parameters['size']: the size of the surface in [rows, columns]
    :type parameters['size']: list

    :return: numpy.array
    """
    slope_step = parameters['slope_step']
    min_value = parameters['min_value']
    size = parameters['size']

    data = numpy.zeros(size, dtype=float)

    for i in range(size[0]):
        data[i, :] = numpy.arange(min_value, size[1], slope_step)

    return data
