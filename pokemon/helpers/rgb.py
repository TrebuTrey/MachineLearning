"""Facilitates interaction with RGB values in images."""

from typing import Tuple

import numpy as np
from PIL.Image import Image


class RGB():
    """Describes a pixel in terms of its RGB (red, green, blue) value."""
    LENGTH = 3
    def __init__(self, pixel: Tuple[int,int,int] = None):
        self.r = 0
        self.g = 0
        self.b = 0
        self.a = None
        if pixel is not None:
            n_val = len(pixel)
            if n_val == self.LENGTH:
                self.r, self.g, self.b = pixel
            elif n_val == self.LENGTH + 1:
                self.r, self.g, self.b, self.a = pixel
            else:
                raise RuntimeError(f"Expected {self.LENGTH} or {self.LENGTH+1} values. Got {n_val}.")
        
    def is_white(self):
        return self.r == 255 and self.g == 255 and self.b == 255

    def is_black(self):
        return self.r == 0 and self.g == 0 and self.b == 0


def compare_img_color(img1: Image, img2: Image) -> float:
    """Compares the color of two images.
    Result is a number between [min=0,max=255*sqrt(3)] where min -> same color and
    max -> opposite color (white vs black)."""
    rgb1 = _get_img_color(img1)
    rgb2 = _get_img_color(img2)
    return _get_color_diff(rgb1, rgb2)


def _get_n_pixels(img: Image) -> int:
    """Obtain the total number of pixels in an image."""
    return int(img.width * img.height)


def _get_color_diff(rgb1: RGB, rgb2: RGB) -> float:
    """Use euclidean distance formula to calculate difference
    between two RGB values."""
    r_dist = int(rgb2.r) - int(rgb1.r)
    g_dist = int(rgb2.g) - int(rgb1.g)
    b_dist = int(rgb2.b) - int(rgb1.b)
    return np.sqrt(pow(r_dist, 2) + pow(g_dist, 2) + pow(b_dist, 2))


def _get_img_color(img: Image, ignore_white: bool = True) -> RGB:
    """Obtain the color of an image as a single RGB value.
    Result is the color averaged over all pixels.
    
    Optionally, ignore white pixels.
    """
    tot_color = RGB()
    n_pixels = _get_n_pixels(img)
    colors = _get_pixel_colors(img)

    for count, pixel in colors:
        rgb = RGB(pixel)
        if ignore_white and rgb.is_white():
            n_pixels -= count
            continue
        tot_color.r += rgb.r*count
        tot_color.g += rgb.g*count
        tot_color.b += rgb.b*count
    rgb_norm = RGB()
    rgb_norm.r = tot_color.r/n_pixels
    rgb_norm.g = tot_color.g/n_pixels
    rgb_norm.b = tot_color.b/n_pixels
    return rgb_norm


def _get_pixel_colors(img: Image):
    if img.palette is None:
        # desired functionality
        return img.getcolors()
    else:
        # if Image is being read in 'P' mode instead of 'RGB' mode,
        # the RGB color counts show up in the Image palette property
        palette_colors = img.palette.colors
        colors = list()
        for (count,color_indx), palette in zip(img.getcolors(), palette_colors):
            color = (count, palette)
            colors.append(color)
        return colors