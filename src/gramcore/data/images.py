"""Imports/exports images and generates artificial ones.

Pythogram-core uses numpy arrays for its operations. This module contains
functions for importing/exporting images, when necessary. It also provides
functions for generating artificial imagery.

Artificial data are PIL Image objects. Measurement units are pixels with
(0, 0) being the top left pixel, (width, 0) the top right and (0, height)
the bottom left.
"""
import numpy
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


def synth_positions(parameters):
    """Calculates the best positions to place the patches in order to create
    a synthetic image.

    It places the patches in a row along the width of the background image
    and not in a grid-like layout. This is why the background is preferable to
    have big width. The patche are aligned to their top.

    Optimal positions in this case are those that maximize the buffer around
    patches. There shouldn't be any overlap of the patches along their width.
    Also, no patch can have height larger than the height of the background.
    The user must provide a background large enough to fit all the patches in,
    otherwise this will return an exception.

    :param parameters['data']: the background image and the patches, first in
                               list is always the background
    :type parameters['data']: PIL.Image

    :return: list of integer positions in [[width, height], [...]] format
    """
    sizes = []
    for img in parameters['data']:
        sizes.append(img.size)
    sizes = numpy.array(sizes)
    bg_size = sizes[0, :]
    patch_sizes = sizes[1::, :]
    patch_nr = patch_sizes.shape[0]

    widths = patch_sizes[:, 0].sum()
    max_height = patch_sizes[:, 1].max()

    if bg_size[0] < widths or bg_size[1] < max_height:
        raise ValueError('Patches too big to fit in the background')

    # these are all ints so the results will be int floors of these
    width_buffer = (bg_size[0] - widths) / (patch_nr + 1)
    height_buffer = (bg_size[1] - max_height) / 2

    positions = []
    current_x = 0
    for patch in range(patch_nr):
        x_pos = current_x + width_buffer
        current_x = x_pos + patch_sizes[patch, 0]
        y_pos = height_buffer
        positions.append([x_pos, y_pos])

    return positions


def synthetic(parameters):
    """Creates an image from a background and smaller patches.

    All input images are converted to RGBA. The alpha channel helps to avoid
    occlusions. The output size equals the size of the background. Patches are
    pasted on the background to given positions. These coordinates refer to
    the top left pixel of each patch. Pasting patches is naive, the user must
    provide suitable patches and positions.

    .. warning::

        Pasting to positions on the boundary of the background will not result
        to an error, but the final image will not include the whole pasted
        patch. Also, in case of overlaps more recent pastes will overwrite
        those beneath them.

    :param parameters['data']: the background image and the patches, first in
                               list is always the background
    :type parameters['data']: PIL.Image
    :param parameters['positions']: Where to place each patch in final image,
                                    given in [[row, column], [...]], if this
                                    is set to 'auto' the positions are
                                    calculated automatically with
                                    synth_positions()
    :type parameters['positions']: list or str
    """
    images = parameters['data']
    positions = []
    if parameters['positions'] is not 'auto':
        positions = parameters['positions']
    else:
        positions = synth_positions({'data': images})

    # convert all input images to RGBA and replace them in th container
    index = 0
    for img in images:
        if img.mode is not 'RGBA':
            images[index] = img.convert('RGBA')
        index += 1

    synth = images.pop(0)
    patches = images
    index = 0
    if len(positions) is len(patches):
        for patch in patches:
            layer = Image.new('RGBA', synth.size)
            layer.paste(patch, tuple(positions[index]))
            synth = Image.composite(layer, synth, layer)
            index += 1
    else:
        if len(positions) > len(patches):
            raise ValueError('More positions than patches')
        else:
            raise ValueError('Less positions than patches')

    return synth


def tiled(parameters):
    """Creates an image by repeating the same image tile.

    This works regardless the size of the tile and the final image. The tile
    is cropped to the image boundaries.

    :param parameters['data']: the basic image to use as tile
    :type parameters['data']: PIL.Image
    :param parameters['size']: [width, height] of the resulting image
    :type parameters['size']: list

    :return: PIL.Image
    """
    tile = parameters['data'][0]
    size = parameters['size']

    img = Image.new(tile.mode, tuple(size))

    w_pos = range(0, size[0], tile.size[0])
    h_pos = range(0, size[1], tile.size[1])

    for w_coord in w_pos:
        for h_coord in h_pos:
            img.paste(tile, (w_coord, h_coord))

    return img
