"""Apply thresholds to arrays.

The following work on 2D arrays.

"""
from skimage import filter


def binary(parameters):
    """Applies a binary threshold to an array

    :param parameters['data'][0]: input array
    :type parameters['data'][0]: numpy.array
    :param parameters['threshold']: the threshold value
    :type parameters['threshold']: integer or float

    :return: numpy.array, with dtype('uint8') containing 0 or 1 values

    """
    data = parameters['data'][0]
    threshold = parameters['threshold']

    result = data > threshold

    return result.astype('uint8')


def otsu(parameters):
    """Calculates the Otsu threshold and applies it to an array

    It wraps `skimage.filter.threshold_otsu`. The `nbins` option is not
    supported.

    :param parameters['data'][0]: input array
    :type parameters['data'][0]: numpy.array

    :return: numpy.array, with dtype('uint8') containing 0 or 1 values

    """
    data = parameters['data'][0]
    threshold = filter.threshold_otsu(data)

    result = data > threshold

    return result.astype('uint8')



