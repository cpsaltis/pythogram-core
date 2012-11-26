"""Tests for module gramcore.datasets.images"""
from PIL import Image
from gramcore.datasets import images

from nose.tools import assert_equal


def test_tiled():
    """Create a tiled image

    Checks for size and color assignment.
    """
    size = [25, 25]
    img = Image.new('RGB', (10, 10))
    img.putpixel((5, 5), (0, 255, 0))
    parameters = {'data': [img], 'size': size}
    tiled = images.tiled(parameters)
    assert_equal(tiled.size, tuple(size))
    assert_equal(tiled.getpixel((5, 5)), (0, 255, 0))
    assert_equal(tiled.getpixel((15, 5)), (0, 255, 0))


def test_synthetic():
    """Create a synthetic image

    Checks for size and color assignment.
    """
    background =  Image.new('RGB', (100, 50), (125, 125, 125))
    red = Image.new('RGB', (10, 5), (255, 0, 0))
    green = Image.new('RGB', (5, 5), (0, 255, 0))
    blue = Image.new('RGB', (20, 5), (0, 0, 255))
    positions = [
        [5, 5],
        [9, 5],
        [99, 20]
    ]

    parameters = {
        'data': [background, red, green, blue],
        'positions': positions
    }

    synth = images.synthetic(parameters)

    assert_equal(synth.getpixel((5, 5)), (255, 0, 0))
    # TODO remember to fix this, patches pasted later override previus values
    assert_equal(synth.getpixel((9, 5)), (255, 255, 0))
