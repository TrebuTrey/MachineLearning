import cv2
import numpy as np

IMG_SIZE = 80


def compare_img(img1_fn: str, img2_fn: str) -> int:
    # read in the images
    img1 = cv2.imread(img1_fn)
    img2 = cv2.imread(img2_fn)

    # resize the images
    img1 = cv2.resize(img1, (IMG_SIZE, IMG_SIZE))
    img2 = cv2.resize(img2, (IMG_SIZE, IMG_SIZE))

    diff = 0
    for arr1, arr2 in zip(img1, img2):
        # unpack into rgb values for each image
        for (r1, g1, b1), (r2, g2, b2) in zip(arr1, arr2):
            # use distance formula to identify differences
            r_dist = int(r2) - int(r1)
            g_dist = int(g2) - int(g1)
            b_dist = int(b2) - int(b1)
            diff += np.sqrt(pow(r_dist, 2) + pow(g_dist, 2) + pow(b_dist, 2))
    print(f"total diff: {diff}")
    return diff


def test_diff_img(img1_fn: str, img2_fn: str):
    img_diff = compare_img(img1_fn, img2_fn)
    assert(img_diff != 0)
    print("images are different")


def test_same_img(img_fn: str):
    img_diff = compare_img(img_fn, img_fn)
    assert(img_diff == 0)
    print("images are same")


if __name__ == "__main__":
    test_img_path_1 = "sprites/002_ivysaur.png"
    test_img_path_2 = "sprites/003_venusaur.png"

    print(f"comparing img to itself: {test_img_path_1}")
    test_same_img(test_img_path_1)

    print(f"comparing imgs: {test_img_path_1} and {test_img_path_2}")
    test_diff_img(test_img_path_1, test_img_path_2)