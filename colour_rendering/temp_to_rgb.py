import numpy as np
from scipy.constants import h, c, k

from colour_rendering.colour_system import cs_hdtv as cs

def planck(lam: np.ndarray, T: int | float):
    """ Returns the spectral radiance of a black body at temperature T.

    Returns the spectral radiance, B(lam, T), in W.sr-1.m-2 of a black body
    at temperature T (in K) at a wavelength lam (in nm), using Planck's law.

    """

    lam_m = lam / 1.e9
    fac = h*c/lam_m/k/T
    B = 2*h*c**2/lam_m**5 / (np.exp(fac) - 1)
    return B

# The grid of visible wavelengths corresponding to the grid of colour-matching
# functions used by the ColourSystem instance.
lam = np.arange(380., 781., 5)

def temp_to_rgb(temp: int | float, out_fmt: str = 'html'): 
    spec = planck(lam, temp)
    rgb = cs.spec_to_rgb(spec, out_fmt=out_fmt)
    return rgb

if __name__ == '__main__': 

    import matplotlib.pyplot as plt
    from matplotlib.patches import Circle

    fig, ax = plt.subplots()

    for i in range(24):
        # T = 500 to 12000 K
        T = 500*i + 500

        # Calculate the black body spectrum and the HTML hex RGB colour string
        # it looks like
        html_rgb = temp_to_rgb(T)

        # Place and label a circle with the colour of a black body at temperature T
        x, y = i % 6, -(i // 6)
        circle = Circle(xy=(x, y*1.2), radius=0.4, fc=html_rgb)
        ax.add_patch(circle)
        ax.annotate('{:4d} K'.format(T), xy=(x, y*1.2-0.5), va='center',
                    ha='center', color=html_rgb)

    # Set the limits and background colour; remove the ticks
    ax.set_xlim(-0.5,5.5)
    ax.set_ylim(-4.35, 0.5)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_facecolor('k')
    # Make sure our circles are circular!
    ax.set_aspect("equal")
    plt.show()