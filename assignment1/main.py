from PIL import Image
import numpy as np
import math
from scipy import signal

from scipy import misc
import matplotlib.pyplot as plt


def boxfilter(n):
    """
    Q 1.1
    :param n: The dimensions of the box filter.
    :return: A numpy nxn array with entries sum to 1.
    """
    # Ensure n is an odd, positive integer.
    assert n % 2 == 1, "Filter dimensions must be odd!"
    assert n > 0, "Filter dimensions must be positive!"
    return np.full((n, n), 1/n**2, dtype=float)


def gauss1d(sigma=1):
    """
    Q 1.2
    :param sigma: The standard deviation of the gaussian distribution that determines the filter.
    :return: A 6*sigma - rounded up to nearest odd integer - sized 1dim numpy array which is a gaussian filter.
    """
    # Ensure sigma is greater than 0.
    assert sigma >= 0, "Sigma must be positive!"
    if math.ceil(6*sigma) % 2 == 1:
        len = math.ceil(6*sigma)
    else:
        len = math.ceil(6*sigma) + 1

    # Edge case, length results in 1x1 matrix.
    if len == 1:
        return np.ones(1)
    else:
        array = np.asarray([math.exp((-float(val)**2)/(2*sigma**2)) for val in range(-int(len/2), int(len/2)+1)])
        return array/np.sum(array)


def gauss2d(sigma=1):
    """
    Q 1.3
    :param sigma: The std.dev. of the gaussian filter.
    :return: a 2d gaussian filter.
    """
    x = gauss1d(sigma)[np.newaxis]
    y = gauss1d(sigma)[np.newaxis].T
    return signal.convolve2d(x, y)


def gaussconvolve2d(array, sigma):
    """
    Q 1.4
    :param array: Input image to apply filter to.
    :param sigma: Std.dev. of the gaussian filter.
    :return: The convolved image.
    """
    f = gauss2d(sigma)
    return signal.convolve2d(array, f, mode="same")


if __name__ == '__main__':

    print("\n\n")

    # == Q 1.1
    '''
    n = 4
    print(f"n = {n}")
    print(boxfilter(n))
    '''

    # ==  Q 1.2 ==
    '''
    for sigma in [0.3, 0.5, 1, 2]:
        f = gauss1d(sigma)
        print("Sigma: ", sigma)
        print(f)
        print("\n\n")
    '''

    # == Q 1.3 ==
    '''
    for sigma in [0.5, 1]:
        f = gauss2d(sigma)
        print(f"Sigma: {sigma}")
        print(f"Filter shape: {f.shape}")
        print(f)
        print("\n\n")
    '''

    # == Q 1.4 ==
    '''
    dog = Image.open("dog.jpg")

    # Convert to numpy array with floating values, scale to [0,1] interval
    image_array = np.asarray(dog.convert("L"), dtype='f')
    image_array /= 255.0

    # Convolve image with filter, scale to [0,255], convert to int..
    result = gaussconvolve2d(image_array, sigma=3)
    
    # Apply filter to input image.
    result = gaussconvolve2d(image_array, sigma=3)

    # Scale to [0,255], convert to int8 array.
    result *= 255.0
    result = result.astype("uint8")

    result_img = Image.fromarray(result)
    result_img.save("dog_result.jpg")

    # Display both images using matplotlib.
    plt.subplot(121)
    plt.title("Original")
    plt.imshow(dog)

    plt.subplot(122)
    plt.title("Filtered")
    plt.imshow(result, cmap="gray")

    plt.show()
    '''

    # == Q 2 ==
    # The low-freq and high-freq images respectively
    img1 = Image.open("0b_dog.bmp")
    img2 = Image.open("0a_cat.bmp")

    plt.subplot(3, 2, 1)
    plt.imshow(img1)

    plt.subplot(3, 2, 2)
    plt.imshow(img2)

    sigma = 5

    # Get color channels from first image as floats, scale to [0,1].
    r, g, b = np.asarray(img1, dtype="f").T/255.0

    # Apply filter to each channel, scale result to [0,255].
    con_r = gaussconvolve2d(r, sigma)*255.0
    con_g = gaussconvolve2d(g, sigma)*255.0
    con_b = gaussconvolve2d(b, sigma)*255.0

    # Merge channels into output image, convert to int8 array.
    img1_low_freq = np.stack((con_r.T, con_g.T, con_b.T), axis=2).astype("uint")

    plt.subplot(3, 2, 3)
    plt.imshow(img1_low_freq)

    # Get color channels from second image as floats, scale to [0,1]
    r, g, b = np.asarray(img2, dtype="f").T/255.0

    # Apply filter to each channel, scale result to [0,255]
    con_r = gaussconvolve2d(r, sigma)*255.0
    con_g = gaussconvolve2d(g, sigma)*255.0
    con_b = gaussconvolve2d(b, sigma)*255.0

    # Merge channels into output image, con
    img2_low_freq = np.stack((con_r.T, con_g.T, con_b.T), axis=2).astype("uint")

    # Compute high freq operation.
    img2_high_freq = img2 - img2_low_freq
    # img2_high_freq = np.clip(img2_high_freq, 0, 255)

    plt.subplot(3, 2, 4)
    plt.imshow(img2_high_freq + 128)

    # TODO Scale all images w/ clip. Create functions per question; test q2 with other images.
    # Get each image's color channels sc apply subtraction
    result = img2_high_freq + img1_low_freq

    # Clip color channels as integers between 0 and 255.
    r, g, b = np.asarray(result, dtype="f").T/255.0
    r = np.clip(r, 0, 1) * 255.0
    g = np.clip(g, 0, 1) * 255.0
    b = np.clip(b, 0, 1) * 255.0

    result = np.stack((r.T, g.T, b.T), axis=2).astype("uint")

    plt.subplot(3, 2, 5)
    plt.imshow(result)

    plt.show()

