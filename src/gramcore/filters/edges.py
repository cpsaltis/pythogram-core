"""Edge extraction filters. These work only on greyscale images."""
from skimage import filter


def canny(parameters):
    """Canny edge extraction filter.

    This wraps `skimage.filter.canny`. The `low_threshold`, `high_threshold`
    and `mask` options are not supported.

    The wrapped function returns a boolean array with pixel values True or
    False. Since it is not very convenient to pass such an array to other
    functions, the return value is cast to uint8, thus containing 0 or 1
    values.

    ..warning::

        During testing there have been some issues with the results. Check the
        corresponding test function for details.

    :param parameters['data'][0]: input image
    :type parameters['data'][0]: numpy.array
    :param parameters['sigma']: standard deviation of the gaussian filter,
                                defaults to 1.0
    :type parameters['sigma']: float

    :return: numpy.array, with dtype('uint8') containing 0 or 1 values

    """
    img = parameters['data'][0]
    sigma = parameters.get('sigma', 1.0)

    result = filter.canny(img, sigma=sigma)

    return result.astype('uint8')


def prewitt(parameters):
    """Prewitt edge extraction filter.

    This wraps `skimage.filter.prewitt`. The `mask` option is not supported.

    The wrapped function returns an array with dtype('float64') and values in
    [0, 1]. Keep this in mind before saving the object as an image file.

    During testing there have been some issues with the results. Check the
    corresponding test function for details.

    (TODO improve this doc string as per sobel below)

    :param parameters['data'][0]: input image
    :type parameters['data'][0]: numpy.array

    :return: numpy.array with dtype('float64')

    """
    img = parameters['data'][0]

    result = filter.prewitt(img)

    return result


def sobel(parameters):
    """Sobel edge extraction filter.

    This wraps `skimage.filter.sobel`. The `mask` option is not supported.

    This produces correct shape though it expands it by one row of pixels
    on every edge. e.g. ideally if the initial image is::

        0 0 0 0 0 0 0
        0 1 1 1 1 1 0
        0 1 1 1 1 1 0
        0 1 1 1 1 1 0
        0 1 1 1 1 1 0
        0 1 1 1 1 1 0
        0 0 0 0 0 0 0

    then after sobel it will become::

        1 1 1 1 1 1 1
        1 1 1 1 1 1 1
        1 1 0 0 0 1 1
        1 1 0 0 0 1 1
        1 1 0 0 0 1 1
        1 1 1 1 1 1 1
        1 1 1 1 1 1 1

    This is to be expected by the way sobel works.

    The wrapped function returns an array with dtype('float64'). If the result
    is cast to another dtype it will not be this accurate. Keep this in mind
    before saving the object as an image file with dtype e.g. uint8.

    :param parameters['data'][0]: input image
    :type parameters['data'][0]: numpy.array

    :return: numpy.array with dtype('float64')

    """
    img = parameters['data'][0]

    result = filter.sobel(img)

    return result
