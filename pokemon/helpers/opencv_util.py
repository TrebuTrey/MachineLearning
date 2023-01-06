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
            self.r, self.g, self.b = pixel
        
    def is_white(self):
        return self.r == 255 and self.g == 255 and self.b == 255

    def is_black(self):
        return self.r == 0 and self.g == 0 and self.b == 0


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


def test_diff_img(img1_fn: str, img2_fn: str):
    img1 = cv2.imread(img1_fn)
    img2 = cv2.imread(img2_fn)
    img_diff = compare_img_pixels(img1, img2)
    assert(img_diff != 0)


def test_same_img(img_fn: str):
    img = cv2.imread(img_fn)
    img_diff = compare_img_pixels(img, img)
    assert(img_diff == 0)
