"""Facilitates interaction with OpenCV objects."""

import cv2
import numpy as np

IMG_SIZE = 80


class RGB():
    """Describes a pixel in terms of its RGB (red, green, blue) value."""
    LENGTH = 3
    def __init__(self, pixel: np.ndarray = None):
        self.r = 0
        self.g = 0
        self.b = 0
        if pixel is not None:
            # OpenCV decoded images have the channels stored in **B G R** order
            self.b, self.g, self.r = pixel
        
    def is_white(self):
        # allow for slightly off-white
        return self.r >= 250 and self.g >= 250 and self.b >= 250

    def is_black(self):
        return self.r == 0 and self.g == 0 and self.b == 0
    
    def max(self):
        return max(self.r, self.g, self.b)
    
    def offset(self, number: float):
        self.r += number
        self.g += number
        self.b += number


def compare_img_color(img1: cv2.Mat,
                      img2: cv2.Mat,
                      ignore_white: bool = True,
                      offset_shading: bool = True) -> float:
    """Compares the color of two images.
    Result is a number between [min=0,max=255*sqrt(3)] where min -> same color and
    max -> opposite color (white vs black)."""
    rgb1 = get_img_color(img1, ignore_white)
    rgb2 = get_img_color(img2, ignore_white)
    
    if offset_shading:
        # offset the values of rgb2 by difference in max from rgb1
        amt_offset = rgb1.max() - rgb2.max()
        rgb2.offset(amt_offset)
    
    return get_color_diff(rgb1, rgb2)


def get_n_pixels(img: cv2.Mat) -> int:
    """Obtain the total number of pixels in an image."""
    return int(img.size/RGB.LENGTH)


def get_image_height(img: cv2.Mat) -> int:
    """Obtain the height of an image, in pixels."""
    return img.shape[0]


def get_image_width(img: cv2.Mat) -> int:
    """Obtain the width of an image, in pixels."""
    return img.shape[1]


def get_color_diff(rgb1: RGB, rgb2: RGB) -> float:
    """Use euclidean distance formula to calculate difference
    between two RGB values."""
    r_dist = int(rgb2.r) - int(rgb1.r)
    g_dist = int(rgb2.g) - int(rgb1.g)
    b_dist = int(rgb2.b) - int(rgb1.b)
    return np.sqrt(pow(r_dist, 2) + pow(g_dist, 2) + pow(b_dist, 2))


def get_img_color(img: cv2.Mat, ignore_white: bool = True) -> RGB:
    """Obtain the color of an image as a single RGB value.
    Result is the color averaged over all pixels.
    
    Optionally, ignore white pixels.
    """
    tot_color = RGB()
    n_pixels = get_n_pixels(img)
    for row in img:
        for pixel in row:
            rgb = RGB(pixel)
            if ignore_white and rgb.is_white():
                n_pixels -= 1
                continue
            tot_color.r += rgb.r
            tot_color.g += rgb.g
            tot_color.b += rgb.b
    rgb_norm = RGB()
    rgb_norm.r = tot_color.r/n_pixels
    rgb_norm.g = tot_color.g/n_pixels
    rgb_norm.b = tot_color.b/n_pixels
    return rgb_norm


def compare_img_pixels(img1: cv2.Mat, img2: cv2.Mat) -> float:
    """Compares two images for pixel equality.
    Result is a number between [min=0,max=unknown] where min -> same image and
    increasing value indicates more differences between the images."""
    # resize the images
    img1 = cv2.resize(img1, (IMG_SIZE, IMG_SIZE))
    img2 = cv2.resize(img2, (IMG_SIZE, IMG_SIZE))

    diff = 0
    for row1, row2 in zip(img1, img2):
        for pixel1, pixel2 in zip(row1, row2):
            # unpack into rgb values for each image
            rgb1 = RGB(pixel1)
            rgb2 = RGB(pixel2)
            diff += get_color_diff(rgb1, rgb2)
    return diff
