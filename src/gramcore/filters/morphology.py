"""Morphological filters.

The following work on 2D arrays. They wrap the relevant scipy functions. The
ones provided by skimage are not well documented for now.

"""
from scipy.ndimage import morphology


def closing(parameters):
    """Calculates morphological closing of a greyscale image.

    This is equal to performing a dilation and then an erosion.

    It wraps `scipy.ndimage.morphology.grey_closing`. The `footprint`,
    `structure`, `output`, `mode`, `cval` and `origin` options are not
    supported.

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
    size = tuple(parameters['size'])

    return morphology.grey_closing(data, size=size)


def erosion(parameters):
    """Erodes a greyscale image.

    For the simple case of a full and flat structuring element, it can be
    viewed as a minimum filter over a sliding window.

    It wraps `scipy.ndimage.morphology.grey_erosion`. The `footprint`,
    `structure`, `output`, `mode`, `cval` and `origin` options are not
    supported.

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
    size = tuple(parameters['size'])

    return morphology.grey_erosion(data, size=size)


def dilation(parameters):
    """Dilates a greyscale image.

    For the simple case of a full and flat structuring element, it can be
    viewed as a maximum filter over a sliding window.

    It wraps `scipy.ndimage.morphology.grey_dilation`. The `footprint`,
    `structure`, `output`, `mode`, `cval` and `origin` options are not
    supported.

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
    size = tuple(parameters['size'])

    return morphology.grey_dilation(data, size=size)


def opening(parameters):
    """Calculates morphological opening of a greyscale image.

    This is equal to performing a dilation and then an erosion.

    It wraps `scipy.ndimage.morphology.grey_closing`. The `footprint`,
    `structure`, `output`, `mode`, `cval` and `origin` options are not
    supported.

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
    size = tuple(parameters['size'])

    return morphology.grey_opening(data, size=size)
