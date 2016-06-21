import matplotlib
matplotlib.rcParams = matplotlib.rc_params_from_file('../../../matplotlibrc')

from matplotlib import pyplot as plt
import solutions
import numpy as np

horse = np.load("horse.npy")[:,::10]

def plotOldNew(old, new, label):
    """Plot an original image and a modified version side by side.

    This plotting script gives better results than the one provided in the
    lab text. Please use this to plot your figures.
    
    Inputs:
        old (2xn ndarray): an array containing the original image's
            x-coordinates on the first row, y-coordinates on the second row.
        new (2xn ndarray): an array containing the transformed image's
            x-coordinates on the first row, y-coordinates on the second row.
        label (str): a title for the transformed image.

    Returns:
        The figure where the images are plotted.
    """
    # Find good boundaries for the plots.
    new_max, old_max = new.max(axis=1), old.max(axis=1)
    new_min, old_min = new.min(axis=1), old.min(axis=1)
    x_max = max((new_max[0], old_max[0])) + 1
    x_min = min((new_min[0], old_min[0])) - 1
    y_max = max((new_max[1], old_max[1])) + 1
    y_min = min((new_min[1], old_min[1])) - 1
    
    fig, (ax1, ax2) = plt.subplots(1, 2, sharey=True)

    # Draw the original image.
    ax1.plot(old[0], old[1], 'k,')
    ax1.axis('equal')
    ax1.set_ylim([y_min, y_max])
    ax1.set_xlim([x_min, x_max])
    ax1.set_xlabel("Original", fontsize=14)

    # Draw the transformed image.
    ax2.plot(new[0], new[1], 'k,')
    ax2.axis('equal')
    ax2.set_ylim([y_min, y_max])
    ax2.set_xlim([x_min, x_max])
    ax2.set_xlabel(label, fontsize=14)
    return fig
    
def stretch():
    fig = plotOldNew(horse, solutions.dilate(horse, 1.5, 1.5), "Dilation")
    fig.savefig("stretch.pdf")
    plt.close(fig.number)

def rotate():
    fig = plotOldNew(horse, solutions.rotate(horse, np.pi/3.), "Rotation")
    fig.savefig("rotate.pdf", format="pdf")
    plt.close(fig.number)
    
def shear():
    fig = plotOldNew(horse, solutions.shear(horse, 0, 1), "Shear")
    fig.savefig("shear.pdf")
    plt.close(fig.number)
    
def reflect():
    fig = plotOldNew(horse, solutions.reflect(horse, [np.sqrt(3), 1]),
                                                                "Reflection")
    fig.savefig("reflect.pdf")
    plt.close(fig.number)
    
def translate():
    fig = plotOldNew(horse, solutions.translate(horse, (0, 2)), "Translation")
    fig.savefig("translate.pdf")
    plt.close(fig.number)
    
def combo():
    p = solutions.shear(horse, -1.02, .5)
    p = solutions.translate(p, np.array([-2, .5]))
    p = solutions.reflect(p, np.array([-2, .5]))
    
    fig = plotOldNew(horse, p, "General Affine")
    fig.savefig("combo.pdf")
    plt.close(fig.number)
    
def trajectory():
    f = solutions.plotTrajectory()
    plt.savefig('soln3.pdf')
    plt.clf()


if __name__ == "__main__":
    stretch()
    rotate()
    shear()
    reflect()
    translate()
    combo()
