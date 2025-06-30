import sys
import numpy as np
from scipy.optimize import minimize
from .colour_system import cs_hdtv

# These are the LEDs for which we have spectral and power data.
all_led_colours = 'red', 'orange', 'green', 'blue'
Pled = {'red': 4.9, 'orange': 1.5, 'green': 1.8, 'blue': 6.3}

# The grid of visible wavelengths corresponding to the grid of colour-matching
# functions used by the ColourSystem instance.
lam = np.arange(380., 781., 5)

def get_led_spectrum_data(filename, lam):
    """Get an LED spectrum from its filename.

    Read in the LED spectrum and interpolate onto wavelengths grid, lam.

    """

    wv, I = [], []
    with open('colour_rendering/' + filename) as fi:
        for line in fi:
            fields = line.split(',')
            wv.append(float(fields[0]))
            I.append(float(fields[1]))

    return np.interp(lam, wv, I)


def get_led_data(led_colours):
    """Get LED and power data for LEDs identified by the provided list."""
    ncolours = len(led_colours)

    # Read in the LED spectra and calculate the LED intensities by weighting
    # with their powers.
    Iled = np.empty((ncolours, lam.shape[0]))
    # LED radiative powers
    for i, led_colour in enumerate(led_colours):
        filename = 'led-{}.csv'.format(led_colour)
        Iled[i] = Pled[led_colour] * get_led_spectrum_data(filename, lam)
    return Iled

def get_led_spec(coeffs, Iled):
    """Calculate an LED spectrum from coefficients to its colour components."""
    return (coeffs * Iled.T).sum(axis=1)

def fit_led_spec(B, Iled):
    """Fit the spectrum B to a linear combination of the LED spectra."""
    A = Iled.T
    coeffs = np.linalg.lstsq(A, B, rcond=None)[0]
    return coeffs, get_led_spec(coeffs, Iled)


def fit_led_xy(B, xy=False, cs=cs_hdtv, led_colours=all_led_colours):
    """
    Find the best linear combination of LED weights to best approximate
    the chromaticity coordinates of a provided spectrum, B. If xy is True,
    these coordinates are passed directly; otherwise deduce them from B and
    the colour matching function.

    """

    # The fit is constrained so that the coefficients are positive.
    ncolours = len(led_colours)

    Iled = get_led_data(led_colours)

    B_xy = B
    if not xy:
        B_xy = cs.spec_to_xyz(B)[:2]

    def minfunc(coeffs):
        """The function to minimize in optimizing the LED colour.

        Create the spectrum as a linear combination of the LED spectra,
        weighted by coeffs, and then return the difference between its
        chromaticity coordinates and the target chromaticity, B_xy.

        Returns the best fit coefficients and the resulting LED spectrum.

        """

        led_spec = get_led_spec(coeffs, Iled)
        led_xy = cs.spec_to_xyz(led_spec)[:2]
        return np.sqrt((B_xy[0]-led_xy[0])**2 + (B_xy[1]-led_xy[1])**2)

    # Optimize the LED spectrum by finding the coefficients which give the
    # closest approximation to the chromaticity coordinates of the target
    # spectrum.
    if not xy:
        # For an initial guess, take the coefficients obtained by a
        # linear, least-squares fit to the target spectrum, if available.
        coeffs, _ = fit_led_spec(B, Iled)
        # Don't allow any negative coefficients.
        coeffs = coeffs.clip(0, None)
    else:
        # Otherwise, just set equal coefficients initially.
        coeffs = np.ones(ncolours) / ncolours
    #print('Initial guess coeffs =', coeffs)

    # NB Late-binding of closures: force the lambdas to take the desired i.
    cons = [{'type': 'ineq',
             'fun': lambda X, i=i: X[i]} for i in range(ncolours)]
    # Add this constraint to prevent pathological fits with all coefficients
    # close to zero:
    cons.append({'type': 'ineq', 'fun': lambda X: np.sum(X)-0.5})
    res = minimize(minfunc, coeffs, constraints=cons, method='COBYLA')
    if not res.success:
        print('Optimization did not suceed. Sorry.')
        sys.exit(1)

    fit_coeffs = res.x
    #print(fit_coeffs)

    led_spec = get_led_spec(fit_coeffs, Iled)
    return fit_coeffs, led_spec