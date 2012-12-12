"""Functions for extracting interest points.

These are applied to numpy.arrays representing images.

"""
import numpy
from skimage import feature


def harris(parameters):
    """Harris interest point operator.

    It wraps `skimage.feature.harris`. The `threshold`, `eps` and
    `gaussian_deviation` options are not supported.

    This function returns an array of 0s and 1s. Harris points are marked
    with 1s. This way the result can be easily transformed to an image. It
    works on RGB and greyscale images.

    The wrapped function returns a set of point coordinates in a list. For
    some reason it is not possible to do something like:

        >>> points = feature.harris(data, min_distance=5)
        >>> data[points] = 1

    so a for loop is used.

    .. note::

        The coordinates returned are not directly on the corner, but a pixel
        inside the object (TODO: is this expected?).

    :param parameters['data'][0]: input array
    :type parameters['data'][0]: numpy.array
    :param parameters['min_distance']: minimum number of pixels separating
                                       interest points and image boundary,
                                       defaults to 10
    :type parameters['min_distance']: float

    :return: numpy.array, it contains 1s where points were found, otherwise 0

    """
    data = parameters['data'][0]
    min_distance = parameters.get('min_distance', 10)

    points = feature.harris(data, min_distance=min_distance)

    result = numpy.zeros((data.shape[0], data.shape[1]), dtype='uint8')

    for point in points:
       result[point[0], point[1]] = 1

    return result
