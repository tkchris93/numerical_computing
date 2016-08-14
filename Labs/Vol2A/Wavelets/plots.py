# plots.py

import numpy as np
from matplotlib import pyplot as plt
from scipy import misc

def grey_image(filename, greyname):
    "Create a grayscale version of a color image"
    image = misc.imread(filename,True)
    plt.imsave(greyname, image, cmap='gray')

def noise_image(filename, noisename):
    "Create a noised version of a grayscale image"
    image = misc.imread(filename,True)
    noiseSigma = 16.0
    image += np.random.normal(0, noiseSigma, size=image.shape)
    plt.imsave(noisename, image, cmap='gray')

# grey_image("swanlake.jpg","swanlake_gray.png")
# noise_image("swanlake_gray.png","swanlake_polluted.png")