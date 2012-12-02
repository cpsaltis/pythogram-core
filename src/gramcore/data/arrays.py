"""Imports/exports arrays and generates artificial ones.

The artificial data are DTMs and DSMs are basically numpy arrays with height
values. All sizes and 2D coordinates refer to array elements, with (0==row,
0==column) being the top left cell.

"""
import numpy
from scipy.ndimage import measurements


def asarray(parameters):
    """Converts a PIL image to a numpy array.

    :param parameters['data']: the input image, takes only one
    :type parameters['data']: PIL.Image

    :return: numpy.array

    """
    return numpy.asarray(parameters['data'][0])


def get_shape(parameters):
    """Returns the shape of the input array.

    :param parameters['data']: the input array, takes only one
    :type parameters['data']: numpy.array

    :return: tuple

    """
    return parameters['data'][0].shape


def gaussian_noise(parameters):
    """Generates gaussian noise.

    .. warning::

        If this is to be applied to images keep in mind that the values should
        be integers and that adding noise will push some pixel values over the
        supports color depth. e.g. In an 8 bit grey image, normally taking
        color values in [0, 255] adding noise to it will make some pixels take
        color values > 255. Scaling these pixels to become white will result
        in more white pixels than expected.

    :param parameters['data']: the input array
    :type parameters['data']: numpy.array
    :param parameters['mean']: mean value of the distribution
    :type parameters['mean']: float
    :param parameters['stddev']: standard deviation of the distribution
    :type parameters['stddev']: float

    :return: numpy.array

    """
    return numpy.random.normal(parameters['mean'],
                               parameters['stddev'],
                               parameters['shape'])


def load(parameters):
    """Loads an array from file and returns it.

    It supports loading from txt and npy files.

    :param parameters['path']: path to the file
    :type parameters['path']: string
    :param parameters['delimiter']: select which delimiter to use for loading
                                    a txt to an array, defaults to space
    :type parameters['delimiter']: string

    :return: numpy.array

    """
    path = parameters['path']
    extension = path.split('.').pop()

    if extension in 'txt':
        delimiter = parameters.get('delimiter', ' ')
        return numpy.loadtxt(path, delimiter=delimiter)
    elif extension in 'npy':
        return numpy.load(path)
    else:
        raise TypeError("Filetype not supported")


def save(parameters):
    """Saves an object to a file.

    It supports saving to txt and npy files.

    :param parameters['data']: the object to be saved, takes only one
    :type parameters['data']: numpy.array
    :param parameters['path']: destination path
    :type parameters['path']: string
    :param parameters['format']: select output format, defaults to '%.2f'
    :type parameters['format']: string
    :param parameters['delimiter']: select which delimiter to use for saving a
                                    txt to an array, defaults to space
    :type parameters['delimiter']: string

    :return: True or raise TypeError

    """
    path = parameters['path']
    data = parameters['data'][0]
    extension = path.split('.').pop()

    if extension in 'txt':
        format = parameters.get('fmt', '%.2f')
        delimiter = parameters.get('delimiter', ' ')
        numpy.savetxt(path, data, fmt=format, delimiter=delimiter)
    elif extension in 'npy':
        numpy.save(path, data)
    else:
        raise TypeError("Filetype not supported")

    return True


def split(parameters):
    """Splits a 3D array and returns only the layer requested.

    :param parameters['data']: the input 3D array, takes only one
    :type parameters['data']: numpy.array
    :param parameters['layer']: the 2D layer to return, 0 is the first one
    :type parameters['layer']: numpy.array

    :return: 2D numpy.array

    """
    return parameters['data'][0][:, :, parameters['layer']]


def dtm(parameters):
    """Generates a DTM with linear slope.

    Slope is applied in row major order, so pixels in each row have the same
    height value.

    :param parameters['slope_step']: height difference for neighbouring cells
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


def dsm(parameters):
    """Generates a DSM by elevating groups a cells by certain height.

    This requires an input array, the DTM, and a mask. The mask designates
    which cells of the DTM should be elevated in order to produce the DSM.
    Basically, the mask shows in which cells there are features with
    significant height, e.g. trees, buildings etc.

    The tricky part it to account for DTM slope when elevating a group of
    cells. If you simply add some height to the initial DTM then the features
    will be elevated parallel to the ground. Especially in the case of
    buildings, their roof is horizontal, regardless of the underlying DTM
    slope.

    To account for this, the algorithm initially labels the mask. As a result
    you get groups of cells which should all be elevated to the same height.
    Next, it finds the maximum height value of underlying DTM for each blob.
    Finally, it assigns `max_blob_height + delta_height` to each blob cell.

    :param parameters['data'][0]: the base DTM
    :type parameters['data'][0]: numpy.array
    :param parameters['data'][1]: the mask of cells to elevate
    :type parameters['data'][1]: numpy.array with boolean/binary values
    :param parameters['delta_height']: single cell elevation value
    :type parameters['delta_height']: float or integer

    :return: numpy.array

    """
    dtm = parameters['data'][0]
    mask = parameters['data'][1]
    delta_height = parameters['delta_height']

    # label and find the max height of each blob
    labels, count = measurements.label(mask)
    max_heights = measurements.maximum(dtm,
                                       labels=labels,
                                       index=range(1, count + 1))

    # assign the max height at each blob cell, required to copy so it won't
    # change the initial dtm values
    dsm = dtm.copy()
    for blob_id in range(1, count + 1):
        dsm[numpy.where(labels == blob_id)] = max_heights[blob_id - 1] +\
                                              delta_height

    return dsm
