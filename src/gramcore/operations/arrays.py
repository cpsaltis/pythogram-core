"""Handling numpy.array data"""
import numpy


def add_gaussian_noise(parameters):
    """Applies gaussian noise to an array.

    :param parameters['data']: the input array
    :type parameters['data']: numpy.array
    :param parameters['mean']: mean value of the distribution
    :type parameters['mean']: float
    :param parameters['stddev']: standard deviation of the distribution
    :type parameters['stddev']: float

    :return: numpy.array
    """
    data = parameters['data'][0]
    noise = numpy.random.normal(parameters['mean'],
                                parameters['stddev'],
                                data.shape)
    return noise + data


def asarray(parameters):
    """Converts a PIL image to a numpy array.

    :param parameters['data']: the input image
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

    :param parameters['data']: the object to be saved
    :type parameters['data']: numpy.array or PIL.Image
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
