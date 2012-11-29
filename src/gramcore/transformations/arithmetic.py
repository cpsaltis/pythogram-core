"""Handling numpy.array data"""
import numpy


def add(parameters):
    """Adds arrays.

    It can add multiple arrays together as long as they all have the same
    dimensions. dtype of the sum is automatically handled by numpy.

    :param parameters['data']: the input arrays, can be more than two
    :type parameters['data']: numpy.array

    :return: sum as a numpy.array
    """
    first_array = parameters['data'][0]
    result = numpy.zeros(first_array.shape)

    for arr in parameters['data']:
        result += arr

    return result


def diff(parameters):
    """Subtracts arrays.

    The first array in data is always the minuend and the second is the
    sudtrahend. dtype of the difference is automatically handled by
    numpy.

    :param parameters['data'][0]: minuend
    :type parameters['data'][0]: numpy.array
    :param parameters['data'][1]: subtrahend
    :type parameters['data'][1]: numpy.array

    :return: difference as a numpy.array
    """
    minuend = parameters['data'][0]
    subtrahend = parameters['data'][1]

    return minuend - subtrahend


def divide(parameters):
    pass


def multiply(parameters):
    pass


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


def ndvi(parameters):
    pass
