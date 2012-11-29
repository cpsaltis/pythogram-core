"""Handling numpy.array data"""
import numpy


def add(parameters):
    """Adds arrays.

    It can add multiple arrays together as long as they all have the same
    dimensions. dtype of the sum is automatically handled by numpy.

    :param parameters['data']: the input arrays, can be more than two
    :type parameters['data']: numpy.array

    :return: numpy.array
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

    :return: numpy.array
    """
    return parameters['data'][0] - parameters['data'][1]


def divide(parameters):
    """Divide arrays, element by element.

    Arrays must have exactly the same dimensions.

    :param parameters['data'][0]: numerator
    :type parameters['data'][0]: numpy.array
    :param parameters['data'][1]: denominator
    :type parameters['data'][1]: numpy.array

    :return: numpy.array
    """
    return parameters['data'][0] / parameters['data'][1]


def ndvi(parameters):
    pass
