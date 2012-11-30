"""Geometric transformations on numpy arrays.

These are useful when the array to be transformed is actually an image.

"""
from skimage import transform


def resize(parameters):
    """Resizes input to match a certain size.

    This wraps `skimage.transform.resize`. For details check:

    http://scikit-image.org/docs/dev/api/skimage.transform.html#resize

    :param parameters['data'][0]: array to resize
    :type parameters['data'][0]: numpy.array
    :param parameters['output_shape']: size of the output
    :type parameters['data'][1]: tuple
    :param parameters['order']: Order of splines used in interpolation.
                                Defaults to 1. For details check
                                `scipy.ndimage.map_coordinates`.
    :type parameters['order']: integer
    :param parameters['mode']: How to handle values outside the image borders.
                               Defaults to 'constant'. For details check
                               `scipy.ndimage.map_coordinates`.
    :type parameters['mode']: string
    :param parameters['cval']: Used in conjunction with mode 'constant', it
                               is the value outside image boundaries. It
                               defaults to 0.0
    :type parameters['cval']: integer or float

    :return: numpy.array

    """
    data = parameters['data'][0]
    output_shape = parameters['output_shape']
    order = parameters.get('order', 1)
    mode = parameters.get('mode', 'constant')
    cval = parameters.get('cval', 0.0)

    return transform.resize(data,
                            output_shape,
                            order=order,
                            mode=mode,
                            cval=cval)


def rotate(parameters):
    """Rotates input anti-clockwise around its center.

    This wraps `skimage.transform.rotate`. For details check:

    http://scikit-image.org/docs/dev/api/skimage.transform.html#rotate

    :param parameters['data'][0]: Array to rotate.
    :type parameters['data'][0]: numpy.array
    :param parameters['angle']: Rotation angle in degrees, counter-clockwise.
    :type parameters['angle']: float
    :param parameters['resize']: Determine whether the shape of the output
                                 image will be automatically calculated, so
                                 the complete rotated image exactly fits.
                                 Defaults to False.
    :type parameters['resize']: bool
    :param parameters['order']: Order of splines used in interpolation.
                                Defaults to 1. For details check
                                `scipy.ndimage.map_coordinates`.
    :type parameters['order']: integer
    :param parameters['mode']: How to handle values outside the image borders.
                               Defaults to 'constant'. For details check
                               `scipy.ndimage.map_coordinates`.
    :type parameters['mode']: string
    :param parameters['cval']: Used in conjunction with mode 'constant', it
                               is the value outside image boundaries. It
                               defaults to 0.0.
    :type parameters['cval']: integer or float

    :return: numpy.array
    """
    data = parameters['data'][0]
    angle = parameters['angle']
    resize_option = parameters.get('resize', False)
    order = parameters.get('order', 1)
    mode = parameters.get('mode', 'constant')
    cval = parameters.get('cval', 0.0)

    return transform.rotate(data,
                            angle,
                            resize=resize_option,
                            order=order,
                            mode=mode,
                            cval=cval)

