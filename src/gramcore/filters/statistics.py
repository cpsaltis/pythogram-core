"""Filters extracting local statistics with a sliding window.

Currently these work only on 2D arrays and they have meaning even if the
underlying array is not an image.

These functions wrap the relevant scipy functions. The ones provided by
skimage are not well documented and they lack a standard deviation filter.

"""
from scipy.ndimage.filters import minimum_filter
from scipy.ndimage.filters import maximum_filter
from scipy.ndimage.filters import uniform_filter
from scipy.ndimage.filters import median_filter
from scipy.ndimage.filters import generic_filter
from scipy.ndimage.measurements import standard_deviation


def minimum(parameters):
    """Calculates the local minimum.

    It wraps `scipy.ndimage.filters.minimum_filter`. The `footprint`,
    `output`, `mode`, `cval` and `origin` options are not supported.

    Keep in mind that `mode` and `cval` influence the results. In this case
    the default mode is used, `reflect`.

    :param parameters['data'][0]: input array
    :type parameters['data'][0]: numpy.array
    :param parameters['size']: which neighbours to take into account, defaults
                               to (3, 3) a.k.a. numpy.ones((3, 3))
    :type parameters['size']: list

    :return: numpy.array

    """
    data = parameters['data'][0]
    size = parameters.get('size', [3, 3])

    return minimum_filter(data, size=tuple(size))


def maximum(parameters):
    """Calculates the local maximum.

    It wraps `scipy.ndimage.filters.minimum_filter`. The `footprint`,
    `output`, `mode`, `cval` and `origin` options are not supported.

    Keep in mind that `mode` and `cval` influence the results. In this case
    the default mode is used, `reflect`.

    :param parameters['data'][0]: input array
    :type parameters['data'][0]: numpy.array
    :param parameters['size']: which neighbours to take into account, defaults
                               to (3, 3) a.k.a. numpy.ones((3, 3))
    :type parameters['size']: list

    :return: numpy.array

    """
    data = parameters['data'][0]
    size = parameters.get('size', [3, 3])

    return maximum_filter(data, size=tuple(size))


def median(parameters):
    """Calculates the local median.

    It wraps `scipy.ndimage.filters.minimum_filter`. The `footprint`,
    `output`, `mode`, `cval` and `origin` options are not supported.

    Keep in mind that `mode` and `cval` influence the results. In this case
    the default mode is used, `reflect`.

    :param parameters['data'][0]: input array
    :type parameters['data'][0]: numpy.array
    :param parameters['size']: which neighbours to take into account, defaults
                               to (3, 3) a.k.a. numpy.ones((3, 3))
    :type parameters['size']: list

    :return: numpy.array

    """
    data = parameters['data'][0]
    size = parameters.get('size', [3, 3])

    return median_filter(data, size=tuple(size))


def average(parameters):
    """Calculates the local average.

    It wraps `scipy.ndimage.filters.minimum_filter`. The `footprint`,
    `output`, `mode`, `cval` and `origin` options are not supported.

    Keep in mind that `mode` and `cval` influence the results. In this case
    the default mode is used, `reflect`.

    :param parameters['data'][0]: input array
    :type parameters['data'][0]: numpy.array
    :param parameters['size']: which neighbours to take into account, defaults
                               to (3, 3) a.k.a. numpy.ones((3, 3))
    :type parameters['size']: list

    :return: numpy.array

    """
    data = parameters['data'][0].astype('float')
    size = parameters.get('size', [3, 3])

    return uniform_filter(data, size=tuple(size))


def stddev(parameters):
    """Calculates the local standard deviation.

    It wraps `scipy.ndimage.filters.minimum_filter`. The `footprint`,
    `output`, `mode`, `cval` and `origin` options are not supported.

    Keep in mind that `mode` and `cval` influence the results. In this case
    the default mode is used, `reflect`.

    :param parameters['data'][0]: input array
    :type parameters['data'][0]: numpy.array
    :param parameters['size']: which neighbours to take into account, defaults
                               to (3, 3) a.k.a. numpy.ones((3, 3))
    :type parameters['size']: list

    :return: numpy.array

    """
    data = parameters['data'][0].astype('float')
    size = parameters.get('size', [3, 3])

    return generic_filter(data, standard_deviation, size=tuple(size))
