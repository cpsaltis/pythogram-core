"""Handling PIL.Image data"""
from PIL import Image


def fromarray(parameters):
    """Converts a numpy array to a PIL image.

    :param parameters['data']: the input array
    :type parameters['data']: numpy.array

    :return: PIL.Image
    """
    return Image.fromarray(parameters['data'][0])


def load(parameters):
    """Loads an image from file and returns it.

    It supports loading from tif, jpg and png.

    :param parameters['path']: path to the file
    :type parameters['path']: string

    :return: PIL.Image
    """
    path = parameters['path']
    extension = path.split('.').pop()

    if extension in ['tif', 'jpg', 'png']:
        return Image.open(path)
    else:
        raise TypeError("Filetype not supported")


def resize(parameters):
    """Resizes an image.

    It supports only Image.NEAREST filter for resampling.

    :param parameters['data']: image to be resized
    :type parameters['data']: PIL.Image
    :param parameters['width']: width of the new image
    :type parameters['width']: integer
    :param parameters['height']: height of the new image
    :type parameters['height']: integer

    :return: PIL.Image
    """
    size = (parameters['width'], parameters['height'])
    return parameters['data'][0].resize(size)


def rotate(parameters):
    """Rotates an image.

    It supports only Image.NEAREST filter for resampling.

    :param parameters['data']: image to be rotated
    :type parameters['data']: PIL.Image
    :param parameters['angle']: clockwise rotation angle in degrees
    :type parameters['angle']: float
    :param parameters['expand']: choose if the the canvas will be expanded to
                                 fit the new image, defaults to 0
    :type parameters['expand']: 0 or 1

    :return: PIL.Image
    """
    angle = parameters['angle']
    expand = parameters.get('expand', 0)
    return parameters['data'][0].rotate(angle, expand=expand)


def save(parameters):
    """Saves an image to a file.

    It supports saving to tif, jpg and png. txt and npy files.

    :param parameters['data']: image to be saved
    :type parameters['data']: PIL.Image
    :param parameters['path']: destination path
    :type parameters['path']: string

    :return: True or raise TypeError
    """
    path = parameters['path']
    data = parameters['data'][0]
    extension = path.split('.').pop()

    if extension in ['tif', 'jpg', 'png']:
        data.save(path)
    else:
        raise TypeError("Filetype not supported")

    return True
