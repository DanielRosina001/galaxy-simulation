import numpy as np
import scipy
import matplotlib.pyplot as plt
import pandas as pd
import math
from scipy.optimize import curve_fit
from scipy.interpolate import CubicSpline


def vector(r, theta, phi): 
    theta = math.radians(theta)
    phi = math.radians(phi)
    x = r*np.sin(phi)*np.cos(theta)
    y = r*np.sin(phi)*np.sin(theta)
    z = r*np.cos(phi)
    return np.array([x,y,z])



df = pd.read_csv('parallax_greater_than_10.csv')
df['distance'] = 1000/df['parallax']
df['absolute_magnitude'] = df['phot_g_mean_mag'] - 5*np.log10(df['distance']/10)

n, bins, patches = plt.hist(df['absolute_magnitude'], np.linspace(min(df['absolute_magnitude']), max(df['absolute_magnitude']), 100))

bin_centers = (bins[:-1] + bins[1:]) / 2
popt, _ = curve_fit(lambda x, a, b, c, d, e, f, g, h, i: a*x**8 + b*x**7 + c*x**6 + d*x**5 + e*x**4 + f*x**3 + g*x**2 + h*x + i, bin_centers, n)

spline = CubicSpline(bin_centers, n)

x_fit = np.linspace(min(bin_centers), max(bin_centers), 100)
y_fit = spline(x_fit)
plt.plot(x_fit, y_fit, color='r', lw=2)


plt.xlim(max(bin_centers), min(bin_centers))
plt.show()
