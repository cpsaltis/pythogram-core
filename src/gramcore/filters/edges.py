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

    During testing there have been some issues with the results. Check the
    corresponding test function for details.

    :param parameters['data'][0]: input image
    :type parameters['data'][0]: numpy.array
    :param parameters['sigma']: standard deviation of the gaussian filter,
                                defaults to 1.0
    :type parameters['sigma']: float

    :return: numpy.array, with dtype('uint8') and 0 or 1 values

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

    :param parameters['data'][0]: input image
    :type parameters['data'][0]: numpy.array

    :return: numpy.array with dtype('float64') and values in [0, 1] range

    """
    img = parameters['data'][0]

    result = filter.prewitt(img)

    return result


def sobel(parameters):
    """Sobel edge extraction filter.

    This wraps `skimage.filter.sobel`. The `mask` option is not supported.

    The wrapped function returns an array with dtype('float64') and values in
    [0, 1]. Keep this in mind before saving the object as an image file.

    During testing there have been some issues with the results. Check the
    corresponding test function for details.

    :param parameters['data'][0]: input image
    :type parameters['data'][0]: numpy.array

    :return: numpy.array with dtype('uint8') and values in [0, 1] range

    """
    img = parameters['data'][0]

    result = filter.sobel(img)

    return result