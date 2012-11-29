"""Imports/exports arrays and generates artificial ones.

The artificial data are DTMs and DSMs are basically numpy arrays with height
values. All sizes and 2D coordinates refer to array elements, with (0==row,
0==column) being the top left cell.
"""
import numpy


def asarray(parameters):
    """Converts a PIL image to a numpy array.

    :param parameters['data']: the input image, takes only one
    :type parameters['data']: PIL.Image

    :return: numpy.array
    """
    return numpy.asarray(parameters['data'][0])


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


def dsm(parameters):
    pass
