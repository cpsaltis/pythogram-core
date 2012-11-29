"""Handling numpy.array data"""
import numpy


def add(parameters):
    """Adds arrays

    :param parameters['data']: the input array
    :type parameters['data']: numpy.array
    :param parameters['mean']: mean value of the distribution
    :type parameters['mean']: float
    :param parameters['stddev']: standard deviation of the distribution
    :type parameters['stddev']: float

    :return: numpy.array
    pass


def diff(parameters):
    pass


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
