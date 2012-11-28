"""Tests for module gramcore.datasets.orthophotos"""
from PIL import Image
from gramcore.datasets import orthophotos

from nose.tools import assert_equal
from nose.tools import raises


def test_tiled():
    """Create a tiled image and check for size and color assignment"""
    size = [25, 25]
    img = Image.new('RGB', (10, 10))
    img.putpixel((5, 5), (0, 255, 0))

    parameters = {'data': [img], 'size': size}

    tiled = orthophotos.tiled(parameters)

    assert_equal(tiled.size, tuple(size))
    assert_equal(tiled.getpixel((5, 5)), (0, 255, 0))
    assert_equal(tiled.getpixel((15, 5)), (0, 255, 0))


def test_synth_positions():
    """Check synth positions with a large background and small patches"""
    background = Image.new('RGB', (30, 20))
    patch_1 = Image.new('RGB', (10, 10))
    patch_2 = Image.new('RGB', (20, 5))

    parameters = {'data': [background, patch_1, patch_2]}

    positions = orthophotos.synth_positions(parameters)

    assert_equal(positions[0][0], 0)
    assert_equal(positions[0][1], 5)
    assert_equal(positions[1][0], 10)
    assert_equal(positions[1][1], 5)


@raises(ValueError)
def test_positions_small_width():
    """Fail in synth_positions because of small backgound width"""
    background = Image.new('RGB', (20, 20))
    patch_1 = Image.new('RGB', (10, 20))
    patch_2 = Image.new('RGB', (11, 20))

    parameters = {'data': [background, patch_1, patch_2]}

    positions = orthophotos.synth_positions(parameters)


@raises(ValueError)
def test_positions_small_height():
    """Fail in synth_positions because of small backgound height"""
    background = Image.new('RGB', (20, 20))
    patch_1 = Image.new('RGB', (10, 21))
    patch_2 = Image.new('RGB', (10, 21))

    parameters = {'data': [background, patch_1, patch_2]}

    positions = orthophotos.synth_positions(parameters)


def test_synthetic():
    """Create a synthetic image and check for size and color assignment

    The two first patches will overlap and the last will be cropped. Notice,
    that overlapping patches overwrite each other and that patches partially
    outside the background are simply cropped and not return an error.
    """
    background = Image.new('RGB', (100, 50), (125, 125, 125))
    red = Image.new('RGB', (10, 5), (255, 0, 0))
    green = Image.new('RGB', (5, 5), (0, 255, 0))
    blue = Image.new('RGB', (20, 5), (0, 0, 255))
    positions = [
        [0, 0],
        [9, 5],
        [99, 20]
    ]

    parameters = {
        'data': [background, red, green, blue],
        'positions': positions
    }

    synth = orthophotos.synthetic(parameters)

    assert_equal(synth.size, (100, 50))
    assert_equal(synth.getpixel((0, 0)), (255, 0, 0, 255))
    # if there was no overwrite of overlapping patches, this should be:
    # assert_equal(synth.getpixel((9, 5)), (255, 255, 0, 255))
    # but since green is pasted last it is:
    assert_equal(synth.getpixel((9, 5)), (0, 255, 0, 255))


def test_synthetic_auto():
    """Create a synthetic image with automatic positions"""
    background = Image.new('RGB', (7, 3), (125, 125, 125))
    red = Image.new('RGB', (1, 1), (255, 0, 0))
    green = Image.new('RGB', (1, 1), (0, 255, 0))
    blue = Image.new('RGB', (1, 1), (0, 0, 255))

    parameters = {
        'data': [background, red, green, blue],
        'positions': 'auto'
    }

    synth = orthophotos.synthetic(parameters)

    assert_equal(synth.size, (7, 3))
    assert_equal(synth.getpixel((1, 1)), (255, 0, 0, 255))
    assert_equal(synth.getpixel((3, 1)), (0, 255, 0, 255))
    assert_equal(synth.getpixel((5, 1)), (0, 0, 255, 255))


@raises(ValueError)
def test_synthetic_less_positions():
    """Fail to create synthetic image, less positions than patches"""
    background = Image.new('RGB', (100, 50))
    patch = Image.new('RGB', (10, 10))
    positions = []

    parameters = {
        'data': [background, patch],
        'positions': positions
    }

    orthophotos.synthetic(parameters)


@raises(ValueError)
def test_synthetic_more_positions():
    """Fail to create synthetic image, more positions than patches"""
    background = Image.new('RGB', (100, 50))
    patch = Image.new('RGB', (10, 10))
    positions = [
        [5, 5],
        [9, 5]
    ]

    parameters = {
        'data': [background, patch],
        'positions': positions
    }

    orthophotos.synthetic(parameters)
