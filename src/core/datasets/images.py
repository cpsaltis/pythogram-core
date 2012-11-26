"""Generates artificial image data.

These are just PIL images so they can be handled with functions from
core.operations.images.
"""
from PIL import Image


def tiled(parameters):
    """Creates an image by repeating the same image tile.

    This works regardless the size of the tile and the final image. The tile
    is cropped at the image boundaries.

    :param parameters['data']: the basic image to use as tile
    :type parameters['data']: PIL.Image
    :param parameters['size']: the size of the image in [width, height]
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


def synth_positions(parameters):
    """Automatically calculates the best positions to place the patches in a
    synthetic image.

    Optimal positions in this case are those that maximize the buffer around
    patches. There shouldn't be any overlap of the patches, otherwise it will
    raise an exception. The user must provide a large enough background for
    the all the patches to fit in. The patches are aligned to their top.

    :param parameters['data']: the background image and the patches, first in
                               list is always the background
    :type parameters['data']: PIL.Image

    :return: list of positions in [[row, column], [...]] format
    """
    sizes = []
    for img in parameters['data'][0]:
        sizes.append(img.size)
    bg_size = numpy.array(sizes[0])
    sizes.remove[sizes[0]]
    patch_sizes = numpy.array(sizes)

    widths = patch_sizes[:, 0].sum()
    heights = patch_sizes[0, :].sum()

    if bg_size[0] < widths and bg_size[1] < heights:
        raise AttributeError('All patches must fit in the background')

    # these are all ints so the x_buffer will be int and the floor of this
    x_buffer = (bg_size[0] - widths) / (patch_sizes.shape[0] + 1)

    positions = []
    current_x = 0
    for patch in sizes:
        x_pos = current_x + x_buffer
        current_x += patch[0]
        y_buffer = (bg_size[1] - patch[1]) / 2
        y_pos = y_buffer
        positions.append([y_pos, x_pos])


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
        patch.

    :param parameters['data']: the background image and the patches, first in
                               list is always the background
    :type parameters['data']: PIL.Image
    :param parameters['positions']: Where to place each patch in final image,
                                    given in [[row, column], [...]], if this
                                    is set to 'auto' the positions are
                                    calculated automatically with
                                    synth_positions()
    :type parameters['positions']: list or str

    TODO: should i make it simpler. without RGBA, it seems occlusions are not
    avoided after all
    """
    background = parameters['data'][0]
    if background.mode not in 'RGBA':
        background = background.convert('RGBA')

    # leave background out but keep the order of patches
    parameters['data'].remove(parameters['data'][0])
    patches = parameters['data']
    for patch in patches:
        if patch.mode not in 'RGBA':
            patch = patch.convert('RGBA')

    positions = []
    if parameters['positions'] is not 'auto':
        positions = parameters['positions']
    else:
        positions = synth_positions({'data': patches.insert(0, background)})

    counter = 0
    synth = background
    if len(positions) is len(patches):
        for patch in patches:
            layer = Image.new('RGBA', synth.size)
            layer.paste(patch, tuple(positions[counter]))
            synth = Image.composite(layer, synth, layer)
            counter += 1
    else:
        raise AttributeError('There should be one position for each patch.')

    return synth
