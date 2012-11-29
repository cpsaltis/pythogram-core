"""Geometric transformations on arrays. They are more useful in the context
that these arrays are in fact images.
"""
from skimage import transform


def resize(parameters):
    """Resizes input to match a certain size.

    Check http://scikit-image.org/docs/dev/api/skimage.transform.html#resize

    :param parameters['data'][0]: array to resize
    :type parameters['data'][0]: numpy.array
    :param parameters['output_shape']: size of the output
    :type parameters['data'][1]: tuple

    :return: numpy.array
    """
    return transform.resize(parameters['data'][0], parameters['output_shape'])


def rotate(parameters):
    """Rotates input anti-clockwise around its center.

    Check http://scikit-image.org/docs/dev/api/skimage.transform.html#rotate

    :param parameters['data'][0]: array to rotate
    :type parameters['data'][0]: numpy.array
    :param parameters['angle']: rotation angle in degrees
    :type parameters['angle']: float
    :param parameters['resize']: expand
    :type parameters['resize']: bool

    :return: numpy.array
    """


