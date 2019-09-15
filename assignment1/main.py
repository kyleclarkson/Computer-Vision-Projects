from PIL import Image
import numpy as np
import math
from scipy import signal

from scipy import misc


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
    # print(boxfilter(3))
    '''
    # ==  Q 1.2 ==
    for sigma in [0.3, 0.5, 1, 2]:
        f = gauss1d(sigma)
        print("Sigma: ", sigma)
        print(f)
        print(np.sum(f))
    '''

    '''
    # == Q 1.3 ==
    for sigma in [0.5, 1]:
        f = gauss2d(sigma)
        print(f"Sigma: {sigma}")
        print(f)
        print(np.sum(f))
    '''

    # TODO 4a question; format; 5
    dog = Image.open("dog.jpg")
    dog.show()

    image_array = np.asarray(dog.convert("L"))

    result = gaussconvolve2d(image_array, 1)
    result = result.astype("uint8")
    result_img = Image.fromarray(result)

    result_img.save("dog_result.jpg")





