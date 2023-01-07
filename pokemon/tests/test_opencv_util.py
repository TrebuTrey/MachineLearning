import os

import cv2

import __init__

from helpers.opencv_util import compare_img_color, compare_img_pixels
from helpers.log import get_logger, mod_fname
logger = get_logger(mod_fname(__file__))

from __init__ import TEST_IMG_DIR
MODULE = os.path.join("helpers", "opencv_util.py")


def test_1_verify_same_img():
    logger.info("Test 1 - verify_same_img")
    img_fn = os.path.join(TEST_IMG_DIR, "cropped_poke_battle_img_1.png")
    img = cv2.imread(img_fn)
    img_diff = compare_img_pixels(img, img)
    assert(img_diff == 0)
    logger.info("Test 1 - success!")


def test_2_verify_diff_img():
    logger.info("Test 2 - verify_diff_img")
    img1_fn = os.path.join(TEST_IMG_DIR, "cropped_poke_battle_img_1.png")
    img2_fn = os.path.join(TEST_IMG_DIR, "cropped_poke_battle_img_2.png")
    img1 = cv2.imread(img1_fn)
    img2 = cv2.imread(img2_fn)
    img_diff = compare_img_pixels(img1, img2)
    assert(img_diff != 0)
    logger.info("Test 2 - success!")


if __name__ == "__main__":
    logger.info(f"Testing {MODULE}")
    test_1_verify_same_img()
    test_2_verify_diff_img()
    logger.info("All tests pass!")